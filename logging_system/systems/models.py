from django.db import models

from locations.models import Location

# Create your models here.
BOOL_CHOICES = [
    (True, 'Yes'),
    (False, 'No')
]
SYSTEM_TYPE_CHOICES = [
    (0, 'Device'),
    (1, 'Computer'),
    (2, 'Server'),
    (3, 'Mobile Phone'),
    (4, 'Network Device'),
    (5, 'Router'),
    (6, 'Switch'),
    (7, 'Access Point'),
    (8, 'IoT'),
    (100, 'Service'),
    (101, 'Virtual Machine'),
    (102, 'Container'),
    (103, 'Web Application'),
    (104, 'Dataabse'),
    (105, 'Backend'),
]

class System(models.Model):
    name                = models.TextField(max_length=50)
    ip                  = models.TextField(max_length=50)
    system_type         = models.IntegerField(choices=SYSTEM_TYPE_CHOICES, default=0)
    port                = models.TextField(max_length=50, null=True, blank=True)
    to_ping             = models.BooleanField(choices=BOOL_CHOICES, default= True)
    last_ping           = models.TextField(max_length=50, null=True)
    last_log            = models.TextField(max_length=50)
    d_count             = models.IntegerField(default=0)
    email_notify        = models.BooleanField(choices=BOOL_CHOICES, default=False)
    graph               = None
    location            = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    service_type        = models.TextField(max_length=50, null=True, blank=True)
    model               = models.TextField(max_length=50, null=True, blank=True)
    notes               = models.TextField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name

class Ping(models.Model):
    date                = models.DateField(auto_now_add=True)
    time                = models.TimeField(auto_now_add=True)
    system              = models.ForeignKey(System, on_delete=models.CASCADE)
    ping                = models.IntegerField(null=True)

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
