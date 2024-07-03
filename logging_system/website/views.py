from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ping3 import ping
from requests import get

from config.models import Settings
from .models import Log, Device, Service
from .forms import SignUpForm, DeviceForm, ServiceForm
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


# devices

def devices(request):
    if request.user.is_authenticated:
        devices = Device.objects.all().order_by("id")

        # update device last_log
        for device in devices:
            device.graph = get_ping_graph(device.ip)
            last_log = Log.objects.filter(host= device.ip).last()
            if last_log is not None:
                device.last_log = last_log.datetime
                device.save()

        paginator = Paginator(devices, 10)
        page_number = request.GET.get("page")
        page_devices = paginator.get_page(page_number)
        
        return render(request, 'devices.html', {'devices': page_devices})
    else:
        return redirect('home')

def device_logs(request, pk):
    if request.user.is_authenticated:

        host = Device.objects.get(id=pk)

        label = request.GET.get('label')
        if label is not None:
            logs = Log.objects.filter(host= host.ip, label=label)
        else:
            logs = Log.objects.filter(host= host.ip)
   
        sort_by = request.GET.get('sort')
        if sort_by in ['datetime', 'host', 'program', 'message']:
            logs = logs.order_by(sort_by)
        else:
            logs = logs.order_by('-id')
            
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(logs, items_per_page)
        page_number = request.GET.get("page")
        page_logs = paginator.get_page(page_number)

        return render(request, 'device_logs.html', {'host': host, 'logs': page_logs, 'label': label, 'sort': sort_by,})
        pass
    else:
        return redirect('home')

def add_device(request):
    if request.user.is_authenticated:
        form = DeviceForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Device added successfully")
                return redirect('devices')
        else:
            return render(request, 'add_device.html', {'form': form})
        return render(request, 'add_device.html', {'form': form})
    else:
        return redirect('home')

def edit_device(request, pk):
    if request.user.is_authenticated:
        update_it = Device.objects.get(id=pk)
        form = DeviceForm(request.POST or None, instance=update_it)
        if form.is_valid():
            form.save()
            messages.success(request, "Device updated successfully")
            return redirect('devices')
        else:
            return render(request, 'edit_device.html', {'form': form})
    else:
        return redirect('home')

def remove_device(request, pk):
    if request.user.is_authenticated:
        delete_it = Device.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Device removed successfully")
        return redirect('devices')
    else:
        return redirect('home')


# services

def services(request):
    if request.user.is_authenticated:
        services = Service.objects.all().order_by('id')

        # update service last_log
        for service in services:
            service.graph = get_ping_graph(service.ip)
            last_log = Log.objects.filter(host= service.ip).last()
            if last_log is not None:
                service.last_log = last_log.datetime
                service.save()

        paginator = Paginator(services, 10)
        page_number = request.GET.get("page")
        page_services = paginator.get_page(page_number)
        
        return render(request, 'services.html', {'services': page_services})
    else:
        return redirect('home')

def service_logs(request, pk):
    if request.user.is_authenticated:
        host = Service.objects.get(id=pk)

        label = request.GET.get('label')
        if label is not None:
            logs = Log.objects.filter(host= host.ip, label=label)
        else:
            logs = Log.objects.filter(host= host.ip)
   
        sort_by = request.GET.get('sort')
        if sort_by in ['datetime', 'host', 'program', 'message']:
            logs = logs.order_by(sort_by)
        else:
            logs = logs.order_by('-id')

        items_per_page = Settings.load().items_per_page
        paginator = Paginator(logs, items_per_page)
        page_number = request.GET.get("page")
        page_logs = paginator.get_page(page_number)

        return render(request, 'service_logs.html', {'host': host, 'logs': page_logs, 'label': label, 'sort': sort_by,})
        pass
    else:
        return redirect('home')

def add_service(request):
    if request.user.is_authenticated:
        form = ServiceForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Service added successfully")
                return redirect('services')
        else:
            return render(request, 'add_service.html', {'form': form})
        return render(request, 'add_service.html', {'form': form})
    else:
        return redirect('home')

def edit_service(request, pk):
    if request.user.is_authenticated:
        update_it = Service.objects.get(id=pk)
        form = ServiceForm(request.POST or None, instance=update_it)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully")
            return redirect('services')
        else:
            return render(request, 'edit_service.html', {'form': form})
    else:
        return redirect('home')

def remove_service(request, pk):
    if request.user.is_authenticated:
        delete_it = Service.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Service removed successfully")
        return redirect('services')
    else:
        return redirect('home')


# validated function

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')