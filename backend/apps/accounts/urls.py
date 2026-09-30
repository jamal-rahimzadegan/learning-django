from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


urlpatterns = [
    # Dashboard
    path("login_user/", views.login_user, name="login"),
    path("logout_user/", views.logout_user, name="logout"),
    path("register_user/", views.register_user, name="register"),

    #Frontend
    path("login", TokenObtainPairView.as_view()),
    path("refresh", TokenRefreshView.as_view()),
]

