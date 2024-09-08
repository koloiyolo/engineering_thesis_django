from celery import shared_task

from .models import System
from .functions import ping_systems

@shared_task
def ping_task ():
    ping_systems(System.objects.filter(to_ping=True))
    return "Objects pinged sucessfully"