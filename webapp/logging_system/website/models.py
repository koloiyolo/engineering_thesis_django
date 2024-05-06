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


class Dataset(models.Model):
    name                = models.TextField(max_length=50)
    count               = models.TextField(max_length=20)
    clusters            = models.TextField(max_length=5)
    data                = models.TextField()

    def save_dataset(self, dataset):
        self.data = json.dumps(dataset)
        self.save()

    def get_dataset(self):
        return list_to_numpy_array(json.loads(self.data))

class MlModel(models.Model):
    name                = models.TextField(max_length=50)
    model_type          = models.TextField(max_length=50)
    args                = models.TextField(max_length=200)
    accuracy            = models.TextField(max_length=10)
    dataset_id          = models.TextField(max_length=20)
    file                = models.BinaryField()