from django.contrib import admin
from .models import Log, Ping

# Register your models here.

admin.site.register(Log)
admin.site.register(Ping)