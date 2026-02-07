from django.urls import path

from . import views

app_name = "incidents"

urlpatterns = [
    path("", views.incidents, name="list"),
    path("<int:tag>", views.incidents, name="list"),
    path("view/<int:pk>", views.view, name="view"),
    path("resolve/<int:pk>", views.resolve, name="resolve"),
    path("remove/<int:pk>", views.remove, name="remove"),
    path("report/<int:frame>", views.report, name="report"),
    path("report/<int:frame>/<int:tag>", views.report, name="report"),
    #    path('path/', views.view, name='name'),
]
