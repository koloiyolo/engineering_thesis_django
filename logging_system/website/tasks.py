from celery import shared_task
from ping3 import ping

from .models import Log, Device, Service, Ping
from .ml import train, classify
from .functions import ping_objects



@shared_task
def ml_classify_task ():
    classify()

@shared_task
def ml_train_task ():
    train()
    
@shared_task
def ping_task ():
    ping_objects(Device.objects.all())
    ping_objects(Service.objects.all())
