from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('datasets/', views.view_datasets, name='datasets'),
    path('add_dataset/', views.add_dataset, name='add_dataset'),
    path('dataset/<int:pk>', views.view_dataset, name='dataset'),
    path('delete_dataset/<int:pk>', views.delete_dataset, name='delete_dataset'),
    path('update_dataset/<int:pk>', views.update_dataset, name='update_dataset'),
    path('models/', views.view_models, name='models'),
    path('add_model/', views.add_model, name='add_model'),
]
