from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import EventForm


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
