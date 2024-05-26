from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Log, Device
from .forms import SignUpForm, DeviceForm

# Create your views here.

def home(request):
    
    logs = None

    sort_by = request.GET.get('sort')
    if sort_by in ['datetime', 'host', 'tags', 'message']:
        logs = Log.objects.all().order_by(sort_by)
    else:
        logs = Log.objects.all()

    paginator = Paginator(logs, 19)
    page_number = request.GET.get("page")
    page_logs = paginator.get_page(page_number)

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
        return render(request, 'home.html', {'logs': page_logs})
    return render(request, 'home.html', {'logs': page_logs})


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
        devices = Device.objects.all()

        # update device last_log
        for device in devices:
            last_log = Log.objects.filter(host= device.ip).last()
            if last_log is not None:
                device.last_log = last_log.datetime
                device.save()

        paginator = Paginator(devices, 12)
        page_number = request.GET.get("page")
        page_devices = paginator.get_page(page_number)
        
        return render(request, 'devices.html', {'devices': page_devices})
    else:
        return redirect('home')

def device_logs(request, pk):
    if request.user.is_authenticated:
        host = Device.objects.get(id=pk)
        logs= Log.objects.filter(host= host.ip).order_by('-id')

        paginator = Paginator(logs, 16)
        page_number = request.GET.get("page")
        page_logs = paginator.get_page(page_number)

        return render(request, 'device_logs.html', {'host': host, 'logs': page_logs})
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

# validated function

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')