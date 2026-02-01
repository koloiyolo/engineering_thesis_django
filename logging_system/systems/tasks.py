from celery import shared_task

from config.models import Settings
from .models import System
from .functions import ping_systems, discover_systems


@shared_task
def ping_task():
    settings = Settings.load()
    settings.ping_interval_ctr += 1
    settings.save()
    if settings.ping_interval_ctr >= settings.ping_interval:
        settings.ping_interval_ctr = 0
        settings.save()
        ping_systems(System.objects.filter(to_ping=True))
        return "Objects pinged sucessfully"


@shared_task
def discover_systems_task(ip_range, system_type=None, prefix=""):
    return f"Task status: {discover_systems(ip_range, system_type=system_type, prefix=prefix)}"
