from django.urls import path, include
from . import views

app_name = 'devices' 

urlpatterns = [
    path('', views.devices, name='list'),
    path('logs/<int:pk>', views.logs, name='logs'),
    path('add/', views.add, name='add'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('remove/<int:pk>', views.remove, name='remove'),
]
