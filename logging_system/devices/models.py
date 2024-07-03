from django.db import models

# Create your models here.

class Device(models.Model):
    name                = models.TextField(max_length=50)
    ip                  = models.TextField(max_length=50)
    port                = models.TextField(max_length=50, null=True)
    last_log            = models.TextField(max_length=50)
    ping                = models.TextField(max_length=50, null=True)
    d_count             = models.IntegerField(default=0)
    email_notify        = models.BooleanField(default=False)
    graph               = None
    model               = models.TextField(max_length=50)
    location            = models.TextField(max_length=50)

class Log(models.Model):
    datetime            = models.TextField(blank=True, null=True)
    host                = models.TextField(blank=True, null=True)
    program             = models.TextField(blank=True, null=True)
    message             = models.TextField(blank=True, null=True)
    label               = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log'

    def get_features(self):
        return f"{self.message} {self.program}"
