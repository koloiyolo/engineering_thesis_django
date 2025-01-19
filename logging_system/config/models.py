from django.db import models
from logs.models import Log

# Create your models here.

from django.core.exceptions import ValidationError

class Settings(models.Model):

    # RadioSelect choices
    ML_CLASSIFIER_CHOICES = [
        (1, 'K-Means'),
        (2, 'Agglomerative Clustering'),
        (3, 'DBSCAN'),
        (4, 'HDBSCAN'),
        (5, 'SOM')
    ]

    ML_VECTORIZER_CHOICES = [
        (0, 'TF-IDF Vectorizer'),
        (1, 'Count Vectorizer'),
    ]

    ML_CLUSTER_CHOICES = [
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    ]
    ML_ANOMALY_CHOICES = [
        (0, '0'),
        (1, '1'),    
    ]

    BOOL_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    NOTIFICATION_CHOICES = [
        (0, 'None'),
        (1, 'System down'),
        (2, 'Log anomaly'),
        (3, 'Both')
    ]

    PAGE_CHOICES = [
        (15, '15'),
        (20,'20'),
        (25,'25'),
        (50,'50'),
        (100,'100')
    ]
    INTERVAL_CHOICES = [
        (1, '1'),
        (3, '3'),
        (6, '6'),
        (12, '12'),
        (24, '24')
    ]

    # Site settings
    site_name = models.CharField(max_length=200, default='My Site')
    maintenance_mode = models.BooleanField(default=False, choices=BOOL_CHOICES)
    contact_email = models.EmailField(default='admin@example.com')
    items_per_page = models.IntegerField(default=20, choices=PAGE_CHOICES)
    
    ping_retries = models.IntegerField(default=5)
    graph_interval = models.IntegerField(default=6, choices=INTERVAL_CHOICES)

    # Notifications settings
    notifications_mode = models.IntegerField(choices=NOTIFICATION_CHOICES, default=0)

    # ML settings
    '''
    s1 - Step 1 Log Grouping

    s2 - Step 2 Outlier/Anomaly Detection
    '''
    s1_vectorizer = models.IntegerField(null=True, blank=True, default=0, choices=ML_VECTORIZER_CHOICES)
    s1_vectorizer_parameters = models.TextField(null=True, blank=True, default=None)
    s1_clusterer = models.IntegerField(null=True, blank=True, default=1, choices=ML_CLASSIFIER_CHOICES)
    s1_clusterer_parameters = models.TextField(null=True, blank=True, default=None)
    s2_vectorizer = models.IntegerField(default=0, choices=ML_VECTORIZER_CHOICES)
    s2_vectorizer_parameters = models.TextField(null=True, blank=True, default=None)
    s2_clusterer = models.IntegerField(default=0, choices=ML_CLASSIFIER_CHOICES)
    s2_clusterer_parameters = models.TextField(null=True, blank=True, default=None)
    on_model_change_reset = models.BooleanField(choices=BOOL_CHOICES, default=False)
    ml_anomaly_cluster = models.IntegerField(default=0, choices=ML_ANOMALY_CHOICES)
    ml_train = models.IntegerField(default=10000)
    ml_classify = models.IntegerField(default = 2000)

    # tracking info
    last_changed_at = models.DateField(auto_now=True)
    # last_changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)


    # Add more fields as needed

    def save(self, *args, **kwargs):
        if Settings.objects.exists():
            if not self.pk and AppSettings.objects.exists():
                raise ValidationError("There can be only one Settings instance.")
            
            if self.pk:
                settings = Settings.load()
                cl1 = settings.s1_clusterer
                cl2 = settings.s2_clusterer
                vec1 = settings.s1_vectorizer
                vec2 = settings.s2_vectorizer

                if (self.on_model_change_reset 
                    and (self.s1_clusterer != cl1
                    or self.s2_clusterer != cl2
                    or self.s1_vectorizer != vec1
                    or self.s2_vectorizer != vec2)):

                    Log.objects.update(label=None)

                    from logs.tasks import ml_train_task
                    ml_train_task.delay(cl=self.s1_clusterer, vec=self.s1_vectorizer)


        
        super().save(*args, **kwargs)

    def __str__(self):
        return "Settings"

    @classmethod
    def load(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance
