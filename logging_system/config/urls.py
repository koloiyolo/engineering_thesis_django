from django.urls import path

from . import views

app_name = "config"

urlpatterns = [
    path("", views.settings, name="settings"),
    path("reset", views.reset, name="reset"),
    path("reset/ml", views.reset_ml, name="reset_ml"),
]
