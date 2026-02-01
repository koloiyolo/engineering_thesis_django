from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "logs"

urlpatterns = [
    path("", views.logs, name="list"),
    path("<int:label>", views.logs, name="list"),
    path("export", views.export, name="export"),
    path("export/<int:pk>", views.export, name="export"),
]
