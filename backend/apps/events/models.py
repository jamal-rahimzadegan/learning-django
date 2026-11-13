from django.db import models
import uuid

class Event(models.Model):
    # 'id' is automatically handled by Django as the primary key
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
        db_table = "events"  # Important: Use your exact Postgres table name

    def __str__(self):
        return self.title


class AppUser(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "users"
        app_label = "events"

    def __str__(self):
        return self.username



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




class Orders(models.Model):
    class Meta:
        db_table = 'orders'

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount_cents = models.PositiveIntegerField()  # e.g. 2500 for €25.00
    currency = models.CharField(max_length=3, default="eur")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)