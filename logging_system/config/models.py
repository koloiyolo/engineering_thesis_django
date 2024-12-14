from django.db import models
from logs.models import Log

# Create your models here.

from django.core.exceptions import ValidationError

class Settings(models.Model):

    # RadioSelect choices
    ML_MODEL_CHOICES = [
        (0, 'K-Means'),
        (1, 'AHC'),
        (2, 'SOM'),
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
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
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


    # Site settings
    site_name = models.CharField(max_length=200, default='My Site')
    maintenance_mode = models.BooleanField(default=False, choices=BOOL_CHOICES)
    contact_email = models.EmailField(default='admin@example.com')
    items_per_page = models.IntegerField(default=20)
    
    ping_retries = models.IntegerField(default=5)

    # Email settings
    notifications_mode = models.IntegerField(choices=NOTIFICATION_CHOICES, default=0)
    email_host = models.CharField(max_length=200, default='smtp.example.com')
    email_port = models.IntegerField(default=465)
    email_host_user = models.CharField(max_length=200, default='from@example.com')
    email_host_password = models.CharField(max_length=200, default='password')
    email_use_ssl = models.BooleanField(default=True, choices=BOOL_CHOICES)
    email_from_address = models.EmailField(default='noreply@example.com')

    # ML settings
    ml_model = models.IntegerField(default=0, choices=ML_MODEL_CHOICES)
    on_model_change_reset_labels = models.BooleanField(choices=BOOL_CHOICES, default=False)
    ml_clusters = models.IntegerField(default=2, choices=ML_CLUSTER_CHOICES)
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
                current = Settings.load().ml_model
                if self.on_model_change_reset_labels and self.ml_model != current:
                    Log.objects.update(label=None)

                    from logs.tasks import ml_train_task
                    ml_train_task.delay(ml_model=current)

                current = Settings.load().ml_clusters
                if self.on_model_change_reset_labels and self.ml_clusters !=  current:
                    Log.objects.update(label=None)

                    from logs.tasks import ml_train_task
                    ml_train_task.delay()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return "Settings"

    @classmethod
    def load(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance
