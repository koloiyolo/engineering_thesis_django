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

class ClassifiedData(models.Model):
    name                = models.TextField(max_length=50)
    model_type          = models.TextField(max_length=20)
    size                = models.TextField(max_length=20)
    offset              = models.TextField(max_length=20)
    date                = models.DateField()
    data                = models.TextField()

    def save_data(self, data):
        self.data = json.dumps(data)
        self.save()

    def get_data(self):
        return list_to_numpy_array(json.loads(self.data))
