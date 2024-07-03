from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from config.models import Settings
from .models import Log, Service
from .forms import ServiceForm
from website.functions import get_ping_graph

# Create your views here.

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

def logs(request, pk):
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

def add(request):
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

def edit(request, pk):
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

def remove(request, pk):
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