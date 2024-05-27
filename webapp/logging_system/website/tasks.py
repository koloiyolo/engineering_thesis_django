from celery import shared_task
from ping3 import ping

from .models import Log, Device, Service, Ping
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
    services = Service.objects.all()
    for device in devices:
        ip = device.ip
        response_time = ping(device.ip, unit='ms')

        if response_time is not None:
            device.ping = f'{int(response_time)} ms'
            device.save()
        else:
            device.ping = None
            device.save()

        Ping.objects.create(ip=ip, ping=response_time)
        
    for service in services:
        ip = service.ip
        response_time = ping(service.ip, unit='ms')

        if response_time is not None:
            service.ping = f'{int(response_time)} ms'
            service.save()
        else:
            service.ping = None
            service.save()

        Ping.objects.create(ip=ip, ping=response_time)

    pass
