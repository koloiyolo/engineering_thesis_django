from django.contrib import admin
from .models import Log, MlModel, Device

# Register your models here.

admin.site.register(Log)
admin.site.register(MlModel)
admin.site.register(Device)