from celery import shared_task

from config.models import Settings

from .ml import classify_som, train_som, classify_ahc, train_ahc, classify_kmeans, train_kmeans



@shared_task
def ml_classify_task (ml_model=None):
    ml_model = Settings.load().ml_model
    if ml_model == 0:
        if classify_kmeans():
            return "KMeans classification complete."
            
        return "KMeans classification failed."
    elif ml_model == 1:
        if classify_ahc():
            return "AHC classification complete."

        return "AHC classification failed."
    else:
        classify_som()
        return "SOM classification complete."

@shared_task
def ml_train_task (ml_model=None):
    if ml_model is None:
        ml_model = Settings.load().ml_model
    if ml_model == 0:
        if train_kmeans():
            return "KMeans training complete."
        return "KMeans training failed."
    elif ml_model == 1:
        if train_ahc():
            return "AHC training complete."
    else:
        train_som()
        return "SOM training complete."
    
