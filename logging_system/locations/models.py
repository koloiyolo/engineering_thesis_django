from django.db import models

# Create your models here.
class Location(models.Model):
    name                = models.TextField(max_length=50)
    address             = models.TextField(max_length=100, null=True)
    room                = models.TextField(max_length=5, null=True)
    notes               = models.TextField(max_length=256, null=True)

    def __str__(self):
        return self.name