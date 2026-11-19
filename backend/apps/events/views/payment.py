import uuid
from datetime import timedelta

import stripe
import time
from django.conf import settings
from django.db import transaction
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Event, Ticket


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

        # lock the event row and reserve a PENDING ticket
        with transaction.atomic():
            try:
                target_event = Event.objects.select_for_update().get(id=event_id)
            except Event.DoesNotExist:
                return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

            if target_event.capacity is not None:
                cutoff = timezone.now() - timedelta(minutes=30)
                active_tickets = (
                        Ticket.objects.filter(event=target_event, status=Ticket.Status.PAID).count()
                        + Ticket.objects.filter(
                    event=target_event,
                    status=Ticket.Status.PENDING,
                    created_at__gte=cutoff,
                ).count()
                )

                if active_tickets >= target_event.capacity:
                    return Response(
                        {"error": "This event is sold out."},
                        status=status.HTTP_409_CONFLICT,
                    )

        return call_stripe(request, target_event)


def call_stripe(request, target_event):
    # Creating the ticket now to reserving the inventory slot before releasing the DB lock
    ticket = Ticket.objects.create(
        user=request.user,
        event=target_event,
        stripe_session_id=f"temp_{uuid.uuid4()}",  # Placeholder until Stripe responds
        status=Ticket.Status.PENDING,
    )

    try:
        # Stripe requires expires_at to be at least 30 minutes in the future
        expires_at = int(time.time()) + (30 * 60)

        session = stripe.checkout.Session.create(
            mode="payment",
            expires_at=expires_at,
            customer_email=request.user.email,
            client_reference_id=str(request.user.id),
            metadata={
                "event_id": str(target_event.id),
                "user_id": str(request.user.id),
                "ticket_id": str(ticket.id),
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

        ticket.stripe_session_id = session.id
        ticket.save(update_fields=["stripe_session_id"])

        return Response({"url": session.url}, status=status.HTTP_201_CREATED)

    except stripe.StripeError as error:
        # Release the reserved spot immediately if Stripe session creation fails
        ticket.status = Ticket.Status.EXPIRED
        ticket.save(update_fields=["status"])
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
