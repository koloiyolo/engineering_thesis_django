from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    # path('models/', views.view_models, name='models'),
    # path('add_model/', views.add_model, name='add_model'),
    path('classify/', views.classify, name='classify'),
    path('classified_data/<int:pk>', views.classified_data, name='classified_data'),
    path('ml_archive', views.ml_archive, name='ml_archive'),
]
