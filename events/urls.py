from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.event_list, name="event_list"),
    path("new/", views.create_event, name="create_event"),
]
