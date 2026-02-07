from django.urls import path

from . import views

app_name = "locations"

urlpatterns = [
    path("", views.locations, name="list"),
    path("add/", views.add, name="add"),
    path("edit/<int:pk>", views.edit, name="edit"),
    path("remove/<int:pk>", views.remove, name="remove"),
]
