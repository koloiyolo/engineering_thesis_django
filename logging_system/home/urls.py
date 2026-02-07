from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health_check, name="health_check"),
    path("", views.home, name="home"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
]
