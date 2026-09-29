from django.urls import path
from utils.route import custom_404_view

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.event_list, name="event_list"),
    path("details/<int:event_id>/", views.event_details, name="event_details"),
    path("new/", views.create_event, name="create_event"),
]

handler404 = custom_404_view
