from celery import shared_task

from .models import System
from .functions import ping_systems, discover_systems

@shared_task
def ping_task ():
    ping_systems(System.objects.filter(to_ping=True))
    return "Objects pinged sucessfully"

@shared_task
def discover_systems_task(ip_range, system_type=None, prefix=""):
    return f"Task status: {discover_systems(ip_range, system_type=system_type, prefix=prefix)}"