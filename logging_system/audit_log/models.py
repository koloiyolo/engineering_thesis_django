from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AuditLog(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=200)