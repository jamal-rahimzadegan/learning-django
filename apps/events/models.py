from django.db import models


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


class User(models.Model):
    # The 'id' field (integer, primary key) is created automatically by Django,
    # so you don't need to explicitly declare it unless you want to override it.

    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
