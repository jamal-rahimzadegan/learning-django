from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.event_list, name="event_list"),
    path("details/<int:event_id>/", views.event_details, name="event_details"),
    path("new/", views.create_event, name="create_event"),
]
