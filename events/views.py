from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import EventForm


def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()  # This instantly saves the record to your Postgres table!
            messages.success(request, "Record successfully created!")
            return redirect("create_event")  # Refresh the page or redirect elsewhere
    else:
        # Show an empty form for a GET request
        form = EventForm()

    return render(request, "create_event.html", {"form": form})
