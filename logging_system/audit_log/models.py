from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AuditLog(models.Model):
    datetime = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=200)