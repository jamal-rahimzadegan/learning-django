# events/management/commands/seed_events.py
import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.events.models import Event


User = get_user_model()

class Command(BaseCommand):
    help = "Bulk-populate Event records for local development or load testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=1000,
            help="Number of events to create (default: 1000)",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help="Number of rows per INSERT query (default: 1000)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing events before seeding",
        )

    def handle(self, *args, **options):
        count: int = options["count"]
        batch_size: int = options["batch_size"]

        # Fetch existing user IDs once—do NOT query or create users inside the loop
        user_ids = list(User.objects.values_list("id", flat=True))
        if not user_ids:
            raise CommandError("No users found. Create at least one user before seeding events.")

        if options["clear"]:
            deleted, _ = Event.objects.all().delete()
            self.stdout.write(f"Deleted {deleted} existing events.")

        now = timezone.now()
        statuses = [choice[0] for choice in Event.Status.choices]
        cities = ["Lisbon", "Porto", "London", "Berlin", "Remote", ""]

        events = [
            Event(
                title=f"Event #{i + 1}: Tech Meetup",
                description="Generated event description for testing.",
                organizer_id=random.choice(user_ids),  # Assign FK ID directly
                status=random.choice(statuses),
                location=random.choice(cities),
                start_time=now + timedelta(days=random.randint(-30, 90)),
                price=random.choice([0, 1000, 2500, 5000, 15000]),
                capacity=random.choice([None, 50, 100, 500]),
            )
            for i in range(count)
        ]

        with transaction.atomic():
            Event.objects.bulk_create(events, batch_size=batch_size)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} events."))
