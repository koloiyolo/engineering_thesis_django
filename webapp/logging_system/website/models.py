from django.db import models
import numpy as np
import json

from .functions import numpy_array_to_list, list_to_numpy_array

# Create your models here.
class Log(models.Model):
    datetime        = models.TextField(blank=True, null=True)
    host            = models.TextField(blank=True, null=True)
    tags            = models.TextField(blank=True, null=True)
    message         = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'


class MlModel(models.Model):
    name                = models.TextField(max_length=50)
    model_type          = models.TextField(max_length=50)
    args                = models.TextField(max_length=200)
