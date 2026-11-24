from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
from apps.events.api.views import EventsViewSet, TicketsViewSet

router = DefaultRouter()
router.register(r"events", EventsViewSet, basename="events")
router.register(r"tickets", TicketsViewSet, basename="tickets")

urlpatterns = [
    re_path(r"^api/(?P<version>[^/]+)/", include(router.urls)),
]