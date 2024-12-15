from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from requests import get
from django.db.models import Q

from logging_system.functions import pagination, logs_short_message
from config.models import Settings
from .models import Log

from systems.models import System


def logs(request, label=None):
    if request.user.is_authenticated:
        
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
    else:
        return redirect('home')

# def logs(request):
#     if request.user.is_authenticated:
#         # Get search query from the request
#         query = request.GET.get('q', '')

#         # Filter logs by case-insensitive partial match if a query exists
#         if query:
#             logs = Log.objects.filter(message__icontains=query)
#         else:
#             logs = Log.objects.all()  # Return all logs if no search query is provided

#         # Pagination setup
#         page = pagination(logs, request.GET.get("page"))

#         # Render the logs with pagination
#         return render(request, 'logs.html', {'logs': page, 'query': query})
#     else:
#         return redirect('home')

# validated function

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     