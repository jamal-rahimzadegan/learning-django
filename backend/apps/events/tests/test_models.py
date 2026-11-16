import pytest

from apps.events.models import  Event, SupportMessage


@pytest.mark.django_db(databases="__all__")
class TestModels:
    def test_event_creation(self):
        event = Event.objects.create(
            title="Summer Party",
            organizer_id=1,
            status="draft",
            price=20,
        )
        assert event.pk is not None
        assert event.title == "Summer Party"
        assert event.organizer_id == 1
        assert event.status == "draft"
        assert event.price == 20
        assert Event._meta.db_table == "events"
        assert str(event) == event.title

    def test_support_msg(self):
        message = SupportMessage.objects.create(
            sender="user",
            text="Hello, I need help with my account.",
        )

        assert message.pk is not None
        assert message.sender == "user"
        assert message.text == "Hello, I need help with my account."
        assert SupportMessage._meta.db_table == "support_messages"
