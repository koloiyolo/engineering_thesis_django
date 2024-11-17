from django.db import models

# Create your models here.
class Location(models.Model):
    name                = models.TextField(max_length=50)
    town                = models.TextField(max_length=100, null=True, blank=True)
    address             = models.TextField(max_length=100, null=True, blank=True)
    room                = models.TextField(max_length=5, null=True, blank=True)
    notes               = models.TextField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name