from django.db import models


class Events(models.Model):
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
        managed = False  # Tells Django NOT to run migrations on this table since it already exists

    def __str__(self):
        return self.title
