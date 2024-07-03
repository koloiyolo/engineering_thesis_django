from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ping3 import ping
from requests import get

from config.models import Settings
from .models import Log
from devices.models import Device
from services.models import Service
from .forms import SignUpForm
from .functions import get_ping_graph, get_labels_graph

# Create your views here.

def home(request):
    
    response = None
    ip = None
    logs = Log.objects.all().order_by("-id")[:5]
    try:
        pass
        response = f"{ping('8.8.8.8', unit='ms'):.3} ms"
        ip = get('https://api.ipify.org').content.decode('utf8')
    except:
        response = None
        ip = None
        
    devices_d = Device.objects.filter(ping=None)
    for device in devices_d:
        device.graph = get_ping_graph(device.ip, width=490)

    services_d = Service.objects.filter(ping=None)
    for service in services_d:
        service.graph = get_ping_graph(service.ip, width=1000)

    labels_graph = get_labels_graph()

    
    data = {'ip': ip,
            'ping': response,
            'logs': logs,
            'devices_d': devices_d, 
            'services_d': services_d,
            'labels_graph': labels_graph}

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
        return render(request, 'home.html', data)
    return render(request, 'home.html', data)


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
        return render(request, 'register.html', {'form': form})
        
    return render(request, 'register.html', {'form': form})


# validated function

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')