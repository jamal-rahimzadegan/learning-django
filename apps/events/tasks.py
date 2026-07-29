from celery import shared_task
from django.utils import timezone


@shared_task
def process_heavy_task(data_id):
    return f"Processed {data_id}"


@shared_task
def run_basic_cron_job():
    # Scheduled to run at specific intervals using Celery beat or triggered manually.
    print(f"Current time: {timezone.now()}")
