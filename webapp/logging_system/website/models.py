from django.db import models
import numpy as np
import json

from .functions import numpy_array_to_list, list_to_numpy_array

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

class Device(models.Model):
    name                = models.TextField(max_length=50)
    ip                  = models.TextField(max_length=50)
    model               = models.TextField(max_length=50)
    location            = models.TextField(max_length=50)
    last_log            = models.TextField(max_length=50)
    ping                = models.TextField(max_length=50, null=True)
    