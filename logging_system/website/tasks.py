from celery import shared_task
from ping3 import ping

from .models import Log, Device, Service, Ping
from config.models import Settings
from .ml import classify_som, train_som, classify_ahc, train_ahc, classify_kmeans, train_kmeans
from .functions import ping_objects



@shared_task
def ml_classify_task ():
    if Settings.load().ml_model == 0:
        classify_kmeans()
        return "KMeans classification complete."
    elif Settings.load().ml_model == 1:
        classify_ahc()
        return "AHC classification complete."
    else:
        classify_som()
        return "SOM classification complete."

@shared_task
def ml_train_task ():
    if Settings.load().ml_model == 0:
        train_kmeans()
        return "KMeans training complete."
    elif Settings.load().ml_model == 1:
        train_ahc()
        return "AHC training complete."
    else:
        train_som()
        return "SOM training complete."
    
@shared_task
def ping_task ():
    ping_objects(Device.objects.all())
    ping_objects(Service.objects.all())
    return "Objects pinged sucessfully"
