from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    # devices
    path('devices/', views.devices, name='devices'),
    path('add_device/', views.add_device, name='add_device'),
    path('edit_device/<int:pk>', views.edit_device, name='edit_device'),
    path('remove_device/<int:pk>', views.remove_device, name='remove_device'),
    path('device_logs/<int:pk>', views.device_logs, name='device_logs'),
    
    # services
    path('services/', views.services, name='services'),
    path('add_service/', views.add_service, name='add_service'),
    path('edit_service/<int:pk>', views.edit_service, name='edit_service'),
    path('remove_service/<int:pk>', views.remove_service, name='remove_service'),
    path('service_logs/<int:pk>', views.service_logs, name='service_logs'),
]
