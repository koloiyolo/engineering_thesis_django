from django.db import models


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50)
    town = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    room = models.CharField(max_length=5, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.name is not None:
            self.name = self.name[:50]
        if self.town is not None:
            self.town = self.town[:100]
        if self.address is not None:
            self.address = self.address[:100]
        if self.notes is not None:
            self.notes = self.notes[:255]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else "Unnamed Location"
