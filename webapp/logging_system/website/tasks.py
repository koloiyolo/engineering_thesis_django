from celery import shared_task
from ping3 import ping

from .models import Log, Device
from .ml import train, classify



@shared_task
def ml_classify ():
    classify()

@shared_task
def ml_train ():
    train()
    
@shared_task
def ping_devices ():
    devices = Device.objects.all()

    for device in devices:
        response_time = ping(device.ip)

        if response_time is not None:
            device.ping = f'{response_time:.3} ms'
            device.save()
        else:
            device.ping = None
            device.save()
    pass
