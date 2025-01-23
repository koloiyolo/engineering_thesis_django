from celery import shared_task

from audit_log.models import AuditLog
from .ml import classify, train
from config.models import Settings


@shared_task
def ml_classify_task ():
    settings = Settings.load()
    settings.ml_classify_interval_ctr += 1
    settings.save()
    if settings.ml_classify_interval_ctr == settings.ml_classify_interval:
        settings.ml_classify_interval_ctr = 0
        settings.save()
        output = classify()
        AuditLog.objects.create(user=None, message=output)
        return output

@shared_task
def ml_train_task (cl=None, vec=None):
    settings = Settings.load()
    settings.ml_train_interval_ctr += 1
    settings.save()
    if settings.ml_train_interval_ctr == settings.ml_train_interval:
        settings.ml_train_interval_ctr = 0
        settings.save()
        output = train(cl=cl, vec=vec)
        AuditLog.objects.create(user=None, message=output)
        return output
    
    
