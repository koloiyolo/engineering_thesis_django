from celery import shared_task

from audit_log.models import AuditLog

from .ml import classify, train



@shared_task
def ml_classify_task (ml_model=None):
    output = classify()
    AuditLog.objects.create(user=None, text=output)
    return output

@shared_task
def ml_train_task (ml_model=None):
    output = train()
    AuditLog.objects.create(user=None, text=output)
    return output
    
    
