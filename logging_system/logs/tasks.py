from celery import shared_task

from logging_system.audit_log.models import AuditLog
from logging_system.config.models import Settings

from .ml import cluster, train


@shared_task
def ml_cluster_task():
    settings = Settings.load()
    settings.ml_cluster_interval_ctr += 1
    settings.save()
    if settings.ml_cluster_interval_ctr >= settings.ml_cluster_interval:
        settings.ml_cluster_interval_ctr = 0
        settings.save()
        output = cluster()
        AuditLog.objects.create(user=None, message=output)
        return output


@shared_task
def ml_train_task(cl=None, vec=None):
    settings = Settings.load()
    settings.ml_train_interval_ctr += 1
    settings.save()
    if (settings.ml_train_interval_ctr >= settings.ml_train_interval) or (cl and vec):
        settings.ml_train_interval_ctr = 0
        settings.save()
        output = train(cl=cl, vec=vec)
        AuditLog.objects.create(user=None, message=output)
        return output
