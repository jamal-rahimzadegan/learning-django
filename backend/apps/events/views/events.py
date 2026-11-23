from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from apps.events.forms import EventForm
from ..models import Event


@staff_member_required
@require_http_methods(["GET", "POST"])
@never_cache
def create_event(request: HttpRequest) -> HttpResponse:
    form = EventForm(request.POST or None, user=request.user)

    if request.method == "POST" and form.is_valid():
        event = form.save(commit=False)
        selected_user = form.cleaned_data["organizer_user"]
        event.organizer_id = selected_user.id
        event.save()

        messages.success(request, "Record successfully created!")
        return redirect("create_event")

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
