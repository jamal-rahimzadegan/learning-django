from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EventViewSet
from . import views



router = DefaultRouter()
router.register(r'list', EventViewSet, basename='') #Define more fore every endpoint

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.event_list, name="event_list"),
    path("details/<int:event_id>/", views.event_details, name="event_details"),
    path("new/", views.create_event, name="create_event"),
    path("api/", include(router.urls)),
]
