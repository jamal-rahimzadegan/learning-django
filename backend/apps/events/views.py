from asyncio import Event

from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django_ratelimit.decorators import ratelimit

from apps.events.forms import EventForm
from apps.events.serializer import EventSerializer
from .models import Event, SupportMessage
from .tasks import process_heavy_task

from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


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
    # return render(request, "events/pages/support.html")
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



# API ViewSet for Event model
class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    # Here you can handle the version
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # Will make it publicly available (includes GET/POST/PUT/UPDATE)
