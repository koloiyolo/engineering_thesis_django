from celery import shared_task
from audit_log.models import AuditLog
from .ml import classify, train


@shared_task
def ml_classify_task ():
    output = classify()
    AuditLog.objects.create(user=None, message=output)
    return output

@shared_task
def ml_train_task (cl=None, vec=None):
    output = train(cl=cl, vec=vec)
    AuditLog.objects.create(user=None, message=output)
    return output
    
    
