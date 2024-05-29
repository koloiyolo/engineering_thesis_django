from django.contrib import admin
from .models import Log, Device, Ping, Service

# Register your models here.

admin.site.register(Log)
admin.site.register(Device)
admin.site.register(Service)
admin.site.register(Ping)