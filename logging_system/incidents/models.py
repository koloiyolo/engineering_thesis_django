from django.db import models
from django.contrib.auth.models import User
from systems.models import System

# Create your models here.

TAG_CHOICES = [
                (0, 'System down'),
                (1, 'Log anomaly detected'),
                ]

class Incident(models.Model):
    date                    = models.DateField(auto_now_add=True)
    time                    = models.TimeField(auto_now_add=True)
    system                  = models.ForeignKey(System, on_delete=models.CASCADE, null=True)
    ip                      = models.TextField(max_length=50)
    tag                     = models.IntegerField(choices=TAG_CHOICES, default=0)
    title                   = models.TextField(max_length=250)
    message                 = models.TextField(max_length=500)

    def __str__(self):
        return self.title

class Comment(models.Model):
    incident                = models.ForeignKey(Incident, on_delete=models.CASCADE)
    date                    = models.DateField(auto_now_add=True)
    time                    = models.TimeField(auto_now_add=True)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    message                 = models.TextField(max_length=250)

    def __str__(self):
        return self.message