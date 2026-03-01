from typing import Any, NamedTuple

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, QuerySet
from django.http import JsonResponse
from django.shortcuts import redirect, render
from ping3 import ping
from requests import get

from logging_system.audit_log.models import AuditLog
from logging_system.config.models import Settings
from logging_system.incidents.models import Incident
from logging_system.logs.models import Log
from logging_system.systems.models import System

from .forms import SignUpForm


# docker compose health check
def health_check(request):
    return JsonResponse({"status": "ok"})


# Create your views here.


class StatisticsData(NamedTuple):
    incident_count: int
    resolved_incidents_count: int
    resolved_incident_ratio: float

    incident_tag0_count: int
    incident_tag0_resolved_count: int
    incident_tag0_resolved_ratio: float

    incident_tag1_count: int
    incident_tag1_resolved_count: int
    incident_tag1_resolved_ratio: float

    log_cont: int
    log_anomaly_count: int
    log_anomaly_ratio: float
    log_devices_anomaly: QuerySet[Log, dict[str, Any]]

    system_count: int
    system_down_count: int
    system_down_ratio: float
    system_systems_down: QuerySet[System, System]


@login_required
def home(request):
    response = None
    ip = None

    incidents = Incident.objects.all().order_by("-id")[: Settings.load().items_per_page]

    try:
        response = f"{ping('8.8.8.8', unit='ms'):.3} ms"
        ip = get("https://api.ipify.org").content.decode("utf8")
    except Exception:
        response = None
        ip = None

    # Incidents
    incident_count = Incident.objects.count()
    resolved_incidents_count = Incident.objects.filter(user__isnull=False).count()

    try:
        resolved_incident_ratio = resolved_incidents_count / incident_count * 100

    except ZeroDivisionError:
        resolved_incident_ratio = 0

    incident_tag0_count = Incident.objects.filter(tag=0).count()
    incident_tag1_count = Incident.objects.filter(tag=1).count()
    incident_tag0_resolved_count = Incident.objects.filter(
        tag=0, user__isnull=False
    ).count()
    incident_tag1_resolved_count = Incident.objects.filter(
        tag=1, user__isnull=False
    ).count()

    try:
        incident_tag0_ratio = incident_tag0_resolved_count / incident_tag0_count * 100

    except ZeroDivisionError:
        incident_tag0_ratio = 0

    try:
        incident_tag1_ratio = incident_tag1_resolved_count / incident_tag1_count * 100

    except ZeroDivisionError:
        incident_tag1_ratio = 0

    # Log
    log_count = Log.objects.count()
    log_anomaly_count = Log.objects.filter(label=0).count()

    try:
        log_anomaly_ratio = log_anomaly_count / log_count * 100
    except ZeroDivisionError:
        log_anomaly_ratio = 0

    log_devices_anomaly = (
        Log.objects.filter(label=0)
        .values("host")
        .annotate(count=Count("host"))
        .order_by("-count")
    )

    # Systems
    system_count = System.objects.count()
    system_down_count = System.objects.filter(d_count__gt=0).count()

    try:
        system_down_ratio = round(system_down_count / system_count * 100)
    except ZeroDivisionError:
        system_down_ratio = 0

    system_systems_down = System.objects.filter(d_count__gt=0).order_by("d_count")[:3]

    statistics = StatisticsData(
        incident_count=incident_count,
        resolved_incidents_count=resolved_incidents_count,
        resolved_incident_ratio=resolved_incident_ratio,
        incident_tag0_count=incident_tag0_count,
        incident_tag0_resolved_count=incident_tag0_resolved_count,
        incident_tag0_resolved_ratio=incident_tag0_ratio,
        incident_tag1_count=incident_tag1_count,
        incident_tag1_resolved_count=incident_tag1_resolved_count,
        incident_tag1_resolved_ratio=incident_tag1_ratio,
        log_cont=log_count,
        log_anomaly_count=log_anomaly_count,
        log_anomaly_ratio=log_anomaly_ratio,
        log_devices_anomaly=log_devices_anomaly,
        system_count=system_count,
        system_down_count=system_down_count,
        system_down_ratio=system_down_ratio,
        system_systems_down=system_systems_down,
    )

    data = {
        "ip": ip,
        "ping": response,
        "incidents": incidents,
        "statistics": statistics,
        # 'logs': logs,
        # 'labels_graph': labels_graph,
        # 'uptime_graph': uptime_graph
    }

    return render(request, "misc/home.html", data)


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            AuditLog.objects.create(
                user=user, message=f"{user} created account successfuly."
            )
            messages.success(request, "You have successfuly created an account!")
            return redirect("home")
        pass
    else:
        form = SignUpForm()
        return render(request, "registration/register.html", {"form": form})

    return render(request, "registration/register.html", {"form": form})
