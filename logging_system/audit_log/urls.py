from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'audit_log'

urlpatterns = [
    path('', views.logs, name='list'),
    path('<int:pk>', views.user, name='user'),
#    path('path/', views.view, name='name'),
]
