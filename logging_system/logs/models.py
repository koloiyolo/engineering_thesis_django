from django.db import models

# Create your models here.

class Log(models.Model):
    datetime            = models.TextField(blank=True, null=True)
    host                = models.TextField(blank=True, null=True)
    program             = models.TextField(blank=True, null=True)
    message             = models.TextField(blank=True, null=True)
    log_group               = models.IntegerField(blank=True, null=True)
    label               = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log'

    def get_features(self):
        return f"{self.message} {self.program}"