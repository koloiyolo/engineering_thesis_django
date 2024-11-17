from django.contrib import admin
from .models import Incident, Comment

# Register your models here.
admin.site.register(Incident)
admin.site.register(Comment)