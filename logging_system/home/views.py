from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from ping3 import ping
from requests import get

from config.models import Settings
from systems.models import System
from incidents.models import Incident
from logs.models import Log
from .forms import SignUpForm
from .functions import get_labels_graph, get_uptime_graph

# docker compose health check
def health_check(request):
    return JsonResponse({'status': 'ok'})

# Create your views here.

def home(request):
    
    response = None
    ip = None

    incidents = Incident.objects.all().order_by("-id")[:5]

    # logs 
    logs = Log.objects.all().order_by("-id")[:10]
    id = 0
    for log in logs:
        log.id = id
        id += 1
        if len(log.message) > 50:
            log.short_message = log.message[:50] + "..."
        else:
            log.short_message = log.message
    # -----

    try:
        response = f"{ping('8.8.8.8', unit='ms'):.3} ms"
        ip = get('https://api.ipify.org').content.decode('utf8')
    except:
        response = None
        ip = None
        
    # systems_d = System.objects.filter(last_ping=None)
    # for system in systems_d:
    #     system.graph = get_ping_graph(system, width=490)


    labels_graph = get_labels_graph()
    uptime_graph = get_uptime_graph()

    
    data = {'ip': ip,
            'ping': response,
            'incidents': incidents,
            'logs': logs,
            'labels_graph': labels_graph,
            'uptime_graph': uptime_graph}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.success(request, "Failed to log in, try again!")
            return redirect('home')

    else:
        return render(request, 'misc/home.html', data)
    return render(request, 'misc/home.html', data)


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfuly created an account!")
            return redirect('home')
        pass
    else:
        form = SignUpForm()
        return render(request, 'auth/register.html', {'form': form})
        
    return render(request, 'auth/register.html', {'form': form})

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