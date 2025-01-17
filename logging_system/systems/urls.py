from django.urls import path, include
from . import views

app_name = 'systems' 

urlpatterns = [
    path('', views.systems, name='list'),
    path('location/<int:location>', views.systems, name='location'),
    path('type/<int:system_type>', views.systems, name='list'),
    path('view/<int:pk>', views.system, name='view'),
    path('logs/<int:pk>', views.logs, name='logs'),
    path('logs/<int:pk>/<int:label>', views.logs, name='logs'),
    path('incidents/<int:pk>', views.incidents, name='incidents'),
    path('incidents/<int:pk>/<int:tag>', views.tag_incidents, name='tag'),
    path('add/', views.add, name='add'),
    path('discover/', views.discover, name='discover'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('remove/<int:pk>', views.remove, name='remove'),
    path('export', views.export_to_csv, name='export'),
    path('export/<int:system_type>', views.export_to_csv, name='export'),
    path('report', views.report, name='report'),
    path('report/<int:system_type>', views.report, name='report'),
]
