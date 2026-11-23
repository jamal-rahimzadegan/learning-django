from django import forms
from django.contrib.auth import get_user_model

from apps.events.models import Event

User = get_user_model()


class EventForm(forms.ModelForm):
    organizer_user = forms.ModelChoiceField(queryset=User.objects.none())

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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["organizer_user"].queryset = User.objects.filter(
                is_active=True
            )
