from datetime import datetime

import stripe
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.db import transaction
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.events.forms import EventForm
from .models import Event, SupportMessage, Ticket
from .serializer import EventSerializer
from .tasks import process_heavy_task


@never_cache
@ratelimit(key='user_or_ip', rate='30/m') #30 req/minute
def index(request):
    process_heavy_task.delay(123)  # Offloads execution immediately
    return render(request, "events/pages/index.html")


@never_cache
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            # Don't save to the DB yet, we need to add the organizer_id
            event = form.save(commit=False)
            # Get the selected user from the form's cleaned data
            selected_user = form.cleaned_data["organizer_user"]
            # Set the organizer_id on the event instance
            event.organizer_id = selected_user.id
            event.save()  # Now save the complete object to the database
            messages.success(request, "Record successfully created!")
            return redirect("create_event")  # Refresh the page or redirect elsewhere
    else:
        form = EventForm()
    return render(request, "events/pages/create_event.html", {"form": form})


# @cache_page(60 * 15)  # caching it for 15 minutes
@never_cache
def event_list(request):
    all_events = Event.objects.all()
    # A simple print statement to prove when the view is actually running
    print("Fetching events from the database and rendering template...")
    return render(request, "events/pages/event_list.html", {"events": all_events})


@never_cache
def event_details(request, event_id):
    cache_key = f"event_{event_id}"
    event = cache.get(cache_key)

    if not event:
        print(f"Event {event_id} not in cache. Fetching from DB.")
        event = Event.objects.get(id=event_id)
        cache.set(cache_key, event, 10)
    else:
        print(f"Event {event_id} found in cache.")

    return render(request, "events/pages/event_details.html", {"event": event})


# Socket
def support(request):
    if request.method == 'POST':
        agent_text = request.POST.get('message', '').strip()

        if agent_text:
            # 1. Save agent message to Database
            SupportMessage.objects.create(sender='agent', text=agent_text)

            # 2. Push message to WebSocket group
            channel_layer = get_channel_layer()
            payload = {
                "id": int(datetime.now().timestamp() * 1000),
                "text": agent_text,
                "sender": "agent",
                "timestamp": datetime.now().strftime("%I:%M %p")
            }

            async_to_sync(channel_layer.group_send)(
                "chat_support_room",
                {
                    "type": "chat_message",
                    "message_data": payload
                }
            )

        return redirect(request.path)

    # Load message history ordered chronologically
    messages = SupportMessage.objects.order_by('created_at')
    return render(request, "events/pages/support.html", {'messages': messages})





class CheckoutTicketStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id: str):
        ticket = get_object_or_404(
            Ticket.objects.select_related("event"),
            stripe_session_id=session_id,
            user=request.user,  # Authorization check: prevents IDOR
        )

        return Response(
            {
                "ticket_id": str(ticket.id),
                "status": ticket.status,
                "event_title": ticket.event.title,
            },
            status=status.HTTP_200_OK,
        )

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        event_id = request.data.get("id")
        if not event_id:
            return Response({"id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        target_event = get_object_or_404(Event, id=event_id)

        try:
            session = stripe.checkout.Session.create(
                mode="payment",
                customer_email=request.user.email,
                client_reference_id=str(request.user.id),
                metadata={
                    "event_id": str(target_event.id),
                    "user_id": str(request.user.id),
                },
                line_items=[
                    {
                        "price_data": {
                            "currency": "eur",
                            "product_data": {"name": target_event.title},
                            "unit_amount": int(target_event.price * 100),
                        },
                        "quantity": 1,
                    }
                ],
                success_url=f"{settings.FRONTEND_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.FRONTEND_URL}/payment/cancel",
            )

            Ticket.objects.create(
                user=request.user,
                event=target_event,
                stripe_session_id=session.id,
                status=Ticket.Status.PENDING,
            )

            return Response({"url": session.url}, status=status.HTTP_201_CREATED)

        except stripe.StripeError as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    if not sig_header:
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except (ValueError, stripe.SignatureVerificationError):
        return HttpResponse(status=400)

    if event.type == "checkout.session.completed":
        session = event.data.object

        if session.payment_status == "paid":
            _fulfill_checkout(session)

    return HttpResponse(status=200)


def _fulfill_checkout(session) -> None:
    session_id = session.id
    metadata = session.metadata or {}

    with transaction.atomic():
        ticket = (
            Ticket.objects.select_for_update()
            .filter(stripe_session_id=session_id)
            .first()
        )

        if ticket:
            if ticket.status == Ticket.Status.PAID:
                return
            ticket.status = Ticket.Status.PAID
            ticket.save(update_fields=["status"])
        else:
            Ticket.objects.get_or_create(
                stripe_session_id=session_id,
                defaults={
                    "user_id": metadata["user_id"],
                    "event_id": metadata["event_id"],
                    "status": Ticket.Status.PAID,
                },
            )





# API ViewSet for Event model
class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    # Here you can handle the version
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # Will make it publicly available (includes GET/POST/PUT/UPDATE)

