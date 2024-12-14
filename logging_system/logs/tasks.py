from celery import shared_task

from config.models import Settings
from audit_log.models import AuditLog

from .ml import classify_som, train_som, classify_ahc, train_ahc, classify_kmeans, train_kmeans



@shared_task
def ml_classify_task (ml_model=None):
    ml_model = Settings.load().ml_model
    if ml_model == 0:
        if classify_kmeans():
            AuditLog.objects.create(user=None, text=f"KMeans classification complete.")
            return "KMeans classification complete."    
            
        AuditLog.objects.create(user=None, text=f"KMeans classification failed.")
        return "KMeans classification failed."
    elif ml_model == 1:
        if classify_ahc():
            AuditLog.objects.create(user=None, text=f"AHC classification complete.")
            return "AHC classification complete."

        AuditLog.objects.create(user=None, text=f"AHC classification failed.")
        return "AHC classification failed."
    else:
        classify_som()
        AuditLog.objects.create(user=None, text=f"SOM classification complete.")
        return "SOM classification complete."
    
    AuditLog.objects.create(user=None, text=f"SOM classification failed.")

@shared_task
def ml_train_task (ml_model=None):
    if ml_model is None:
        ml_model = Settings.load().ml_model
    if ml_model == 0:
        if train_kmeans():
            AuditLog.objects.create(user=None, text=f"KMeans training complete.")
            return "KMeans training complete."
        
        AuditLog.objects.create(user=None, text=f"KMeans training failed.")
        return "KMeans training failed."
    elif ml_model == 1:
        if train_ahc():
            AuditLog.objects.create(user=None, text=f"AHC training complete.")
            return "AHC training complete."

        AuditLog.objects.create(user=None, text=f"AHC training failed.")
        return "AHC training failed."
    else:
        if train_som():
            AuditLog.objects.create(user=None, text=f"SOM training complete.")
            return "SOM training complete."

        AuditLog.objects.create(user=None, text=f"SOM training failed.")
        return "SOM training complete."

    AuditLog.objects.create(user=None, text=f"Training failed.")
    return "Training failed."
    
    
