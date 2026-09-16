from asyncio import Event

from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

from apps.events.forms import EventForm
from apps.events.serializer import EventSerializer

from .models import Event
from .tasks import process_heavy_task

def index(request):
    process_heavy_task.delay(123)  # Offloads execution immediately
    return render(request, "events/pages/index.html")


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


@cache_page(60 * 15) #caching it for 15 minutes
def event_list(request):
    all_events = Event.objects.all()
    # A simple print statement to prove when the view is actually running
    print("Fetching events from the database and rendering template...")
    return render(request, "events/pages/event_list.html", {"events": all_events})


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




# API ViewSet for Event model


class EventViewSet(viewsets.ModelViewSet):
    # 1. Define where the view gets its data from
    queryset = Event.objects.all()
    
    # 2. Tell the view which serializer to use for formatting the data
    serializer_class = EventSerializer