from celery import shared_task


@shared_task
def process_heavy_task(data_id):
    # Your heavy computation or API call here
    return f"Processed {data_id}"
