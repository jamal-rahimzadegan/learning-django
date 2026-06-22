from django.urls import path

from . import views

urlpatterns = [
    path("new-event/", views.create_event, name="create_event"),
]
