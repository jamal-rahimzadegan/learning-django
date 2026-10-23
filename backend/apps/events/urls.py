from django.urls import path, re_path

from core.utils.route import custom_404_view
from . import views, consumers

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.event_list, name="event_list"),
    path("support/", views.support, name="support"),
    path("details/<int:event_id>/", views.event_details, name="event_details"),
    path("new/", views.create_event, name="create_event"),
]

websocket_urlpatterns = [
re_path(r"^ws/support/$", consumers.SupportChatConsumer.as_asgi()),
]

handler404 = custom_404_view
