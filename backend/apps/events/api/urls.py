from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from apps.events.api.views import EventsViewSet, TicketsViewSet

events_router = DefaultRouter()
tickets_router = DefaultRouter()
events_router.register(r"", EventsViewSet, basename="")
tickets_router.register(r"", TicketsViewSet, basename="tickets")

urlpatterns = [
    re_path(r"^api/(?P<version>[^/]+)/events/", include(events_router.urls)),
    re_path(r"^api/(?P<version>[^/]+)/tickets/", include(tickets_router.urls)),
]
