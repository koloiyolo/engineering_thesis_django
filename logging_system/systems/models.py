from django.db import models

from locations.models import Location

# Create your models here.
BOOL_CHOICES = [(True, "Yes"), (False, "No")]
SYSTEM_TYPE_CHOICES = [
    (0, "Device"),
    (1, "Computer"),
    (2, "Server"),
    (3, "NAS"),
    (4, "Mobile Phone"),
    (5, "Network Device"),
    (6, "Router"),
    (7, "Switch"),
    (8, "Access Point"),
    (9, "IoT"),
    (10, "NVR"),
    (11, "CCTV"),
    (100, "Service"),
    (101, "Virtual Machine"),
    (102, "Container"),
    (103, "Web Application"),
    (104, "Dataabse"),
    (105, "Backend"),
]


class System(models.Model):
    name = models.CharField(max_length=50)
    ip = models.CharField(max_length=50)
    system_type = models.IntegerField(choices=SYSTEM_TYPE_CHOICES, default=0)
    port = models.CharField(max_length=50, null=True, blank=True)
    to_ping = models.BooleanField(choices=BOOL_CHOICES, default=True)
    last_ping = models.CharField(max_length=50, null=True)
    last_log = models.CharField(max_length=50)
    d_count = models.IntegerField(default=0)
    email_notify = models.BooleanField(choices=BOOL_CHOICES, default=False)
    graph = None
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    service_type = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    notes = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name


class Ping(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    ping = models.IntegerField(null=True)
