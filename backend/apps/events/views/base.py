from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit

from apps.events.tasks import process_heavy_task


@never_cache
@ratelimit(key='user_or_ip', rate='30/m')  # 30 req/minute
def index(request):
    process_heavy_task.delay(123)  # Offloads execution immediately
    return render(request, "events/pages/index.html")
