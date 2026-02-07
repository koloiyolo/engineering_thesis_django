from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "audit_log"

urlpatterns = [
    path("", views.logs, name="list"),
    path("<int:user>", views.logs, name="list"),
    path("report/<int:frame>", views.report, name="report"),
    path("report/<int:frame>/<int:user>", views.report, name="report"),
    #    path('path/', views.view, name='name'),
]
