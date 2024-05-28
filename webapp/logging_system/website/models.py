from django.db import models
from django.utils.translation import gettext_lazy as _
import numpy as np
import json

# Create your models here.
class Log(models.Model):
    datetime            = models.TextField(blank=True, null=True)
    host                = models.TextField(blank=True, null=True)
    tags                = models.TextField(blank=True, null=True)
    message             = models.TextField(blank=True, null=True)
    label               = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'

    def get_features(self):
        return f"{self.message} {self.tags}"

class BaseInfo(models.Model):
    name                = models.TextField(max_length=50)
    ip                  = models.TextField(max_length=50)
    port                = models.TextField(max_length=50, null=True)
    last_log            = models.TextField(max_length=50)
    ping                = models.TextField(max_length=50, null=True)
    graph               = None

    class Meta:
        abstract = True

class Device(BaseInfo):
    model               = models.TextField(max_length=50)
    location            = models.TextField(max_length=50)

class Service(BaseInfo):
    service_type        = models.TextField(max_length=50)


class Ping(models.Model):
    ip                  = models.TextField(max_length=50)
    ping                = models.IntegerField(null=True)