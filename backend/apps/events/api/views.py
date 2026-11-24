from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from apps.events.models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class EventsViewSet(viewsets.ModelViewSet):
    print('events api')
    serializer_class = EventSerializer
    # Allows anyone to GET, requires login for POST/PUT/PATCH/DELETE
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Deterministic ordering matches your composite DB index (-created_at, -id)
        return (
            Event.objects
            .filter(status=Event.Status.PUBLISHED)
            .select_related("organizer")
            .order_by("-created_at", "-id")
        )


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]
