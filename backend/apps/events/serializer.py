from rest_framework import serializers
from .models import Event, AppUser  # Adjust import based on your User model location

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
