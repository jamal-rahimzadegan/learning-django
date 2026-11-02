import pytest
from pytest_django.asserts import assertContains


@pytest.mark.django_db(databases="__all__")
class TestEventViews:
    def test_index_loads(self, client):
        response = client.get("/events/")
        assert response.status_code == 200
        assertContains(response, "Home page content goes here.")

    def test_list_loads(self, client):
        response = client.get("/events/list/")
        assert response.status_code == 200
        assertContains(response, "Event List")

    def test_support_loads(self, client):
        response = client.get("/events/support/")
        assert response.status_code == 200
        assertContains(response, "Support tickets")





