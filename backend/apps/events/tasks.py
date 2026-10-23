from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

logger = get_task_logger(__name__)


@shared_task
def process_heavy_task(data_id):
    return f"Processed {data_id}"


@shared_task
def run_basic_cron_job():
    # Scheduled to run at specific intervals using Celery beat or triggered manually.
    logger.info(f"-----Current time: {timezone.now()}-----")
