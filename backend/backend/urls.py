from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from apps.events.views import EventsViewSet, TicketsViewSet

admin.site.site_header = "Social event"
admin.site.site_title = "Social event"
admin.site.index_title = "Welcome to Social event Admin Portal"

events_router = DefaultRouter()
tickets_router = DefaultRouter()
events_router.register(r"", EventsViewSet, basename="")
tickets_router.register(r"", TicketsViewSet, basename="tickets")


# It's for testing Sentry
def trigger_error(request):
    division_by_zero = 1 / 0


basic = [
    path("admin/", admin.site.urls),
]

api_spec = [
    path(
        "api/schema/", SpectacularAPIView.as_view(), name="schema"
    ),  # 1. Downloadable Schema endpoint (YAML/JSON)
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),  # 2. Interactive Swagger UI
    path(
        "api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),  # 3. Alternative Redoc UI (great for reading documentation)
]

events = [
    path("events/", include("apps.events.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("", RedirectView.as_view(url="/events/", permanent=True)),
    re_path(r"^api/(?P<version>[^/]+)/events/", include(events_router.urls)),
    re_path(r"^api/(?P<version>[^/]+)/tickets/", include(tickets_router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
    path('sentry-debug/', trigger_error),
]

urlpatterns = basic + events + api_spec
