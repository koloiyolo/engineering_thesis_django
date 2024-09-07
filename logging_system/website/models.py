from django.db import models
from django.utils.translation import gettext_lazy as _
import numpy as np
import json

# Create your models here.

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


class Ping(models.Model):
    date                = models.DateField(auto_now_add=True)
    ip                  = models.TextField(max_length=50)
    ping                = models.IntegerField(null=True)

