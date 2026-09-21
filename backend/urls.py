from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

admin.site.site_header = "Social event"
admin.site.site_title = "Social event"
admin.site.index_title = "Welcome to Social event Admin Portal"


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
    path("", RedirectView.as_view(url="/events/", permanent=True)),
]

urlpatterns = basic + events + api_spec
