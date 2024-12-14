from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from requests import get
from django.db.models import Q

from config.models import Settings
from .models import Log

from systems.models import System


def logs(request):
    if request.user.is_authenticated:
        logs = None
        q = request.GET.get('search', '')
        if q:
            logs = logs.filter(
                Q(host__icontains=q) |
                Q(program__icontains=q) |
                Q(message__icontains=q)
            ).order_by('-id')
        else:
            logs = Log.objects.order_by('-id')

        items_per_page = Settings.load().items_per_page
        paginator = Paginator(logs, items_per_page)
        page_number = request.GET.get("page")
        page_logs = paginator.get_page(page_number)
        clusters = Log.objects.filter(label__isnull=False).values_list('label', flat=True).distinct()
        id = 0
        for log in page_logs:
            log.id = id
            id += 1
            if len(log.message) > 50:
                log.short_message = log.message[:50] + "..."
            else:
                log.short_message = log.message

        hosts = Log.objects.all().values_list('host', flat=True).distinct()
        systems = []
        for host in hosts:
            systems.append(System.objects.filter(ip=host).first())
        data = {
            'systems': systems,
            'logs': page_logs,
            'clusters': clusters}
        return render(request, 'misc/logs.html', data)
    else:
        return redirect('home')

def label(request, label):
    if request.user.is_authenticated:
        logs = None
        q = request.GET.get('search', '')
        if q:
            logs = logs.filter(
                Q(host__icontains=q) |
                Q(program__icontains=q) |
                Q(message__icontains=q),
                label=label
            ).order_by('-id')
        else:
            logs = Log.objects.filter(label=label).order_by('-id')

        if not logs.exists():
            messages.warning(request, f"Label '{label}' is empty!")
            return redirect('logs')
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(logs, items_per_page)
        page_number = request.GET.get("page")
        page_logs = paginator.get_page(page_number)
        clusters = Log.objects.filter(label__isnull=False).values_list('label', flat=True).distinct()
        id = 0
        for log in page_logs:
            log.id = id
            id += 1
            if len(log.message) > 50:
                log.short_message = log.message[:50] + "..."
            else:
                log.short_message = log.message

        hosts = Log.objects.all().values_list('host', flat=True).distinct()
        systems = []
        for host in hosts:
            systems.append(System.objects.filter(ip=host).first())
        data = {
            'systems': systems,
            'logs': page_logs,
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
#         items_per_page = Settings.load().items_per_page
#         paginator = Paginator(logs, items_per_page)

#         # Get the current page number (default to page 1 if not provided)
#         page_number = request.GET.get("page", 1)
#         page_logs = paginator.get_page(page_number)

#         # Render the logs with pagination
#         return render(request, 'logs.html', {'logs': page_logs, 'query': query})
#     else:
#         return redirect('home')

# validated function

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     