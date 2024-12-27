from django.db import models
from django.contrib.auth.models import User
from systems.models import System

# Create your models here.

TAG_CHOICES = [
                (0, 'System down'),
                (1, 'Log anomaly'),
                ]

class Incident(models.Model):
    date                    = models.DateField(auto_now_add=True)
    time                    = models.TimeField(auto_now_add=True)
    system                  = models.ForeignKey(System, on_delete=models.CASCADE, null=True)
    ip                      = models.CharField(max_length=50)
    tag                     = models.IntegerField(choices=TAG_CHOICES, default=0)
    title                   = models.CharField(max_length=255)
    message                 = models.CharField(max_length=255)
    user                    = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,  default=None)

    def save(self, *args, **kwargs):
        if self.ip:
            self.ip = self.ip[:50]
        if self.title:
            self.title = self.title[:255]
        if self.message:
            self.message = self.message[:255]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    incident                = models.ForeignKey(Incident, on_delete=models.CASCADE)
    date                    = models.DateField(auto_now_add=True)
    time                    = models.TimeField(auto_now_add=True)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    message                 = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.message:
            self.message = self.message[:255]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.message