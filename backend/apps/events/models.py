from django.db import models
from django.conf import settings
import uuid

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    organizer_id = models.BigIntegerField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    price = models.IntegerField()
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "events"

    def __str__(self):
        return self.title


class SupportMessage(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('agent', 'Support Agent'),
    ]

    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'support_messages'

    def __str__(self):
        return f"{self.sender}: {self.text[:30]}"


class Ticket(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        REFUNDED = "refunded", "Refunded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets"
    )
    event = models.ForeignKey(
        "Event", on_delete=models.PROTECT, related_name="tickets"
    )
    stripe_session_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tickets'
        indexes = [models.Index(fields=["user", "event"])]

