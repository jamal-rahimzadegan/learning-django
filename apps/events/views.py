from asyncio import Event

from django.contrib import messages
from django.shortcuts import redirect, render

from apps.events.forms import EventForm

from .models import Event


def index(request):
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


def event_list(request):
    all_events = Event.objects.all()
    return render(request, "events/pages/event_list.html", {"events": all_events})


def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, "events/pages/event_details.html", {"event": event})
