from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from requests import get

from config.models import Settings
from .models import Log


def logs(request):
    if request.user.is_authenticated:
        query = request.GET.get('q', '')  # Get the search query from the request
        logs = Log.objects.filter(message__icontains=query).order_by('-id')  # Filter items by name
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
        return render(request, 'logs.html', {'logs': page_logs, 'clusters': clusters})
    else:
        return redirect('home')

def label(request, label):
    if request.user.is_authenticated:
        query = request.GET.get('q', '')  # Get the search query from the request
        logs = Log.objects.filter(label=label, message__icontains=query).order_by('-id')  # Filter items by name
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
        return render(request, 'logs.html', {'logs': page_logs, 'clusters': clusters})
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