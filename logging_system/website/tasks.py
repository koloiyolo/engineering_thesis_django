from celery import shared_task
from ping3 import ping

from .models import Log, Device, Service, Ping
from .ml import classify_som, train_som, train_ahc, classify_ahc
from .functions import ping_objects



@shared_task
def ml_classify_task ():
    classify_ahc()

@shared_task
def ml_train_task ():
    train_ahc()
    
@shared_task
def ping_task ():
    ping_objects(Device.objects.all())
    ping_objects(Service.objects.all())
