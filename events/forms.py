from django import forms

from events.models import Event, User


class EventForm(forms.ModelForm):
    # Create a dropdown field populated with users.
    # This field is not part of the Events model, so we define it here.
    organizer_user = forms.ModelChoiceField(
        queryset=User.objects.all(), label="Organizer", required=True
    )

    class Meta:
        model = Event

        fields = [
            "title",
            "description",
            "status",
            "location",
            "start_time",
            "price",
            "capacity",
        ]
        # Optional: Add a date/time picker widget for the start_time field
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
