from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from website.functions import get_ping_graph
from .models import Device, Log
from config.models import Settings
from .forms import DeviceForm
# Create your views here.

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

def logs(request, pk):
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

def add(request):
    if request.user.is_authenticated:
        form = DeviceForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Device added successfully")
                return redirect('devices:list')
        else:
            return render(request, 'add_device.html', {'form': form})
        return render(request, 'add_device.html', {'form': form})
    else:
        return redirect('home')

def edit(request, pk):
    if request.user.is_authenticated:
        update_it = Device.objects.get(id=pk)
        form = DeviceForm(request.POST or None, instance=update_it)
        if form.is_valid():
            form.save()
            messages.success(request, "Device updated successfully")
            return redirect('devices:list')
        else:
            return render(request, 'edit_device.html', {'form': form})
    else:
        return redirect('home')

def remove(request, pk):
    if request.user.is_authenticated:
        delete_it = Device.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Device removed successfully")
        return redirect('devices:list')
    else:
        return redirect('home')

# validated function

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')
