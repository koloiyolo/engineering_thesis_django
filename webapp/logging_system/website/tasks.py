from celery import shared_task

from .models import Log
from .ml import train, classify

@shared_task
def ml_classify ():
    classify()

@shared_task
def ml_train ():
    train()
    
