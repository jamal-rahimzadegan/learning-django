from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.events.models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer


# API ViewSet for Event model
class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    # Here you can handle the version
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # Will make it publicly available (includes GET/POST/PUT/UPDATE)


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]
