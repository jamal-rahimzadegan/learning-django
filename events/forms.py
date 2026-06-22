from django import forms

from events.models import Events


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        # We exclude 'id' and 'created_at' because the database handles those automatically
        fields = [
            "title",
            "description",
            "organizer_id",
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
