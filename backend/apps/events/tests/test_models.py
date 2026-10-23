import pytest
from apps.events.models import AppUser

@pytest.mark.django_db(databases="__all__")
def test_create_app_user():
    user = AppUser.objects.create(
        username="johndoe",
        email="john@example.com",
        password="hashed_password_here"
    )
    assert user.pk is not None