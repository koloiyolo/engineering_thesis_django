from django.urls import path, include
from . import views

app_name = 'systems' 

urlpatterns = [
    path('', views.systems, name='list'),
    path('export', views.export, name='export'),
    path('location/<int:location>', views.systems, name='location'),
    path('type/<int:system_type>', views.systems, name='type'),
    path('view/<int:pk>', views.system, name='view'),
    path('logs/<int:pk>', views.logs, name='logs'),
    path('logs/<int:pk>/<int:label>', views.logs, name='label'),
    path('incidents/<int:pk>', views.incidents, name='incidents'),
    path('incidents/<int:pk>/<int:tag>', views.tag_incidents, name='tag'),
    path('add/', views.add, name='add'),
    path('discover/', views.discover, name='discover'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('remove/<int:pk>', views.remove, name='remove'),
]
