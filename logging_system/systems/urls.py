from django.urls import path, include
from . import views

app_name = 'systems' 

urlpatterns = [
    path('', views.systems, name='list'),
    path('location/<int:location>', views.location, name='location'),
    path('view/<int:pk>', views.system, name='view'),
    path('logs/<int:pk>', views.logs, name='logs'),
    path('logs/<int:pk>/<int:label>', views.label, name='label'),
    path('incidents/<int:pk>', views.incidents, name='incidents'),
    path('incidents/<int:pk>/<int:tag>', views.tag_incidents, name='tag'),
    path('add/', views.add, name='add'),
    path('discover/', views.discover, name='discover'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('remove/<int:pk>', views.remove, name='remove'),
]
