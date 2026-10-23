import os

from celery import Celery

# Replace 'backend' with your actual Django project directory name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# Cron jobs
app.conf.beat_schedule = {
    "run_basic_cron_job_every_5_seconds": {
        "task": "apps.events.tasks.run_basic_cron_job",
        "schedule": 5.0,
    },
}
