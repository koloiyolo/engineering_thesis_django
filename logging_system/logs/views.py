from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from requests import get
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from logging_system.functions import pagination, logs_short_message
from config.models import Settings
from .models import Log
from .forms import ExportToCsvForm
from .functions import export_csv

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
    return render(request, 'log/list.html', data)


@login_required
def export(request, pk=None):
    system = None
    if pk is not None:
        system = System.objects.get(id=pk)

    form = ExportToCsvForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            file_name = form.cleaned_data.get("file_name") if form.cleaned_data.get("file_name") else "" 
            count = form.cleaned_data.get("count") if form.cleaned_data.get("count") else None
            labels = form.cleaned_data.get("with_labels")

            logs = None
            if system is None:
                print("None")
                logs = Log.objects.all()
            else:
                print("not None")
                logs = Log.objects.filter(host=system.ip)
            
            response = export_csv(logs, count=count, file_name=file_name, labels=labels)
            return response
    else:
        return render(request, 'log/export.html', {'form': form})
    return render(request, 'log/export.html', {'form': form})





    if system:
        return redirect(f"system:logs {system.id}")
    else:
        return redirect(f"logs:list")