"""
URL configuration for logging_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("logging_system.home.urls")),
    path("settings/", include("logging_system.config.urls")),
    path("logs/", include("logging_system.logs.urls")),
    path("systems/", include("logging_system.systems.urls")),
    path("incidents/", include("logging_system.incidents.urls")),
    path("locations/", include("logging_system.locations.urls")),
    path("audit_log/", include("logging_system.audit_log.urls")),
    # path('incidents/', include('incidents.urls')),
]
