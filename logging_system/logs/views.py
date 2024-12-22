from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from requests import get
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from logging_system.functions import pagination, logs_short_message
from config.models import Settings
from .models import Log

from systems.models import System

@login_required
def logs(request, label=None):
    logs = None
    q = request.GET.get('search', '')
    if label is not None:
        if q:
            logs = Log.objects.filter(
                Q(host__icontains=q) |
                Q(program__icontains=q) |
                Q(message__icontains=q),
                label=label
            ).order_by('-id')
        else:
            logs = Log.objects.filter(label=label).order_by('-id')
    else:
        if q:
            logs = Log.objects.filter(
                Q(host__icontains=q) |
                Q(program__icontains=q) |
                Q(message__icontains=q)
            ).order_by('-id')
        else:
            logs = Log.objects.order_by('-id')
    page = pagination(logs, request.GET.get("page"))
    clusters = Log.objects.filter(label__isnull=False).values_list('label', flat=True).distinct()
    
    page = logs_short_message(page)
    hosts = Log.objects.all().values_list('host', flat=True).distinct()
    systems = []
    for host in hosts:
        systems.append(System.objects.filter(ip=host).first())
    data = {
        'systems': systems,
        'logs': page,
        'clusters': clusters}
    return render(request, 'misc/logs.html', data)
