from django.urls import path
from utils.route import custom_404_view

from . import views


urlpatterns = [
    path("login_user/", views.login_user, name="login"),
]

