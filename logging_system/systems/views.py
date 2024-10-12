from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from website.functions import get_ping_graph
from .models import System
from website.models import Log
from config.models import Settings
from .forms import SystemForm
# Create your views here.

def systems(request):
    if request.user.is_authenticated:
        systems = System.objects.all().order_by("id")

        # update system last_log
        for system in systems:
            system.graph = get_ping_graph(system)
            last_log = Log.objects.filter(host= system.ip).last()
            if last_log is not None:
                system.last_log = last_log.datetime
                system.save()

        paginator = Paginator(systems, 10)
        page_number = request.GET.get("page")
        page_systems = paginator.get_page(page_number)
        
        return render(request, 'systems.html', {'systems': page_systems})
    else:
        return redirect('home')

def logs(request, pk):
    if request.user.is_authenticated:

        host = System.objects.get(id=pk)
        query = request.GET.get('q', '')  # Get the search query from the request
        logs = Log.objects.filter(host=host.ip, message__icontains=query)  # Filter items by name
        if logs.count() is 0:
            messages.warning(request, f"Label '{label}' is empty!")
            return redirect('logs')
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(logs, items_per_page)
        page_number = request.GET.get("page")
        page_logs = paginator.get_page(page_number)
        for log in page_logs:
            if len(log.message) > 90:
                log.short_message = log.message[:90] + "..."
            else:
                log.short_message = log.message
        return render(request, 'system_logs.html', {'host': host, 'logs': page_logs})
        pass
    else:
        return redirect('home')

def label(request, pk, label):
    if request.user.is_authenticated:
        host = System.objects.get(id=pk)
        query = request.GET.get('q', '')  # Get the search query from the request
        logs = Log.objects.filter(host=host.ip, label=label, message__icontains=query)  # Filter items by name
        if logs.count() is 0:
            messages.warning(request, f"Label '{label}' is empty!")
            return redirect('systems:logs', host.id)
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(logs, items_per_page)
        page_number = request.GET.get("page")
        page_logs = paginator.get_page(page_number)
        for log in page_logs:
            if len(log.message) > 90:
                log.short_message = log.message[:90] + "..."
            else:
                log.short_message = log.message
        return render(request, 'system_logs.html', {'host': host, 'logs': page_logs})
        pass
    else:
        return redirect('home')

# query = request.GET.get('q', '')  # Get the search query from the request
#         logs = Log.objects.filter(label=label, message__icontains=query)  # Filter items by name
#         if logs.count() is 0:
#             messages.warning(request, f"Label '{label}' is empty!")
#             return redirect('logs')

def add(request):
    if request.user.is_authenticated:
        form = SystemForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "System added successfully")
                return redirect('systems:list')
        else:
            return render(request, 'add_system.html', {'form': form})
        return render(request, 'add_system.html', {'form': form})
    else:
        return redirect('home')

def edit(request, pk):
    if request.user.is_authenticated:
        update_it = System.objects.get(id=pk)
        form = SystemForm(request.POST or None, instance=update_it)
        if form.is_valid():
            form.save()
            messages.success(request, "System updated successfully")
            return redirect('systems:list')
        else:
            return render(request, 'edit_system.html', {'form': form})
    else:
        return redirect('home')

def remove(request, pk):
    if request.user.is_authenticated:
        delete_it = System.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "System removed successfully")
        return redirect('systems:list')
    else:
        return redirect('home')

# validated function

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')
