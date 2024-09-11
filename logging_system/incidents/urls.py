from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'incidents'

urlpatterns = [
    path('', views.incidents, name='list'),
    path('view/<int:pk>', views.view, name='view'),
    path('remove/<int:pk>', views.remove, name='remove'),
#    path('path/', views.view, name='name'),
]
