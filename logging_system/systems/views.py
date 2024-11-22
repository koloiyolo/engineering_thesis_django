from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib import messages

from .functions import get_ping_graph

from .models import System
from incidents.models import Incident
from logs.models import Log
from locations.models import Location
from config.models import Settings
from .forms import SystemForm
# Create your views here.

def systems(request):
    if request.user.is_authenticated:
        systems = System.objects.all().order_by("id")

        # update system last_log
        for system in systems:
            last_log = Log.objects.filter(host= system.ip).last()
            if last_log is not None:
                system.last_log = last_log.datetime
                system.save()
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(systems, items_per_page)
        page_number = request.GET.get("page")
        page_systems = paginator.get_page(page_number)
        locations = Location.objects.all()
        data = {
            'systems': page_systems,
            'locations': locations
        }
        return render(request, 'system/list.html', data)
    else:
        return redirect('home')

def location(request, location):
    if request.user.is_authenticated:
        systems = System.objects.filter(location=location)
        if not systems.exists():
            messages.warning(request, f"There are no systems located in {location}!")
            return redirect('systems')
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(systems, items_per_page)
        page_number = request.GET.get("page")
        page_systems = paginator.get_page(page_number)
        locations = Location.objects.all()
        data = {
            'systems': page_systems,
            'locations': locations
        }
        return render(request, 'system/list.html', data)
    else:
        return redirect('home')   

def system(request, pk):
    if request.user.is_authenticated:
        system = System.objects.get(id=pk)
        system.graph = get_ping_graph(system)
        last_log = Log.objects.filter(host=system.ip).last()
        if last_log is not None:
            system.last_log = last_log.datetime
            system.save()

        system.graph = get_ping_graph(system)

        # logs
        logs = Log.objects.filter(host=system.ip).order_by("-id")[:10]
        clusters = Log.objects.filter(label__isnull=False).values_list('label', flat=True).distinct()
        for log in logs:
            if len(log.message) > 50:
                log.short_message = log.message[:50] + "..."
            else:
                log.short_message = log.message
        # -----

        incidents = Incident.objects.filter(system=system).order_by("-id")[:5]

        data = {
            'system': system,
            'logs': logs,
            'clusters': clusters,
            'incidents': incidents
        }
        return render(request, 'system/view.html', data)
    else:
        return redirect('home')

def logs(request, pk):
    if request.user.is_authenticated:

        system = System.objects.get(id=pk)
        query = request.GET.get('q', '')  # Get the search query from the request
        logs = Log.objects.filter(host=system.ip, message__icontains=query).order_by('-id')  # Filter items by name
        if not logs.exists():
            messages.warning(request, f"Label '{label}' is empty!")
            return redirect('logs')
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(logs, items_per_page)
        page_number = request.GET.get("page")
        page_logs = paginator.get_page(page_number)
        clusters = Log.objects.filter(label__isnull=False).values_list('label', flat=True).distinct()
        for log in page_logs:
            if len(log.message) > 50:
                log.short_message = log.message[:50] + "..."
            else:
                log.short_message = log.message
        return render(request, 'system/logs.html', {'system': system, 'logs': page_logs, 'clusters': clusters})
        pass
    else:
        return redirect('home')


def label(request, pk, label):
    if request.user.is_authenticated:
        system = System.objects.get(id=pk)
        query = request.GET.get('q', '')  # Get the search query from the request
        logs = Log.objects.filter(host=system.ip, label=label, message__icontains=query).order_by('-id')  # Filter items by name
        if logs.count() == 0:
            messages.warning(request, f"Label '{label}' is empty!")
            return redirect('systems:logs', system.id)
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(logs, items_per_page)
        page_number = request.GET.get("page")
        page_logs = paginator.get_page(page_number)
        clusters = Log.objects.filter(label__isnull=False).values_list('label', flat=True).distinct()
        for log in page_logs:
            if len(log.message) > 50:
                log.short_message = log.message[:50] + "..."
            else:
                log.short_message = log.message
        return render(request, 'system/logs.html', {'system': system, 'logs': page_logs, 'clusters': clusters})
        pass
    else:
        return redirect('home')

def incidents(request, pk):
    if request.user.is_authenticated:
        system = System.objects.get(id=pk)

        incidents = Incident.objects.filter(system=system).order_by("-id")
        if not incidents.exists():
            messages.warning(request, f"There are no incidents for {system.name}")
            return redirect(reverse('systems:view', args=[system.id]))
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(incidents, items_per_page)
        page_number = request.GET.get("page")
        page_incidents = paginator.get_page(page_number)
        return render(request, 'system/incidents.html', {'system': system, 'incidents': page_incidents})
        pass
    else:
        return redirect('home')

def tag_incidents(request, pk, tag):
    if request.user.is_authenticated:
        system = System.objects.get(id=pk)

        query = request.GET.get('q', '')
        incidents = Incident.objects.filter(system=system, tag=tag, ip__icontains=query).order_by("-id")
        if not incidents.exists():
            messages.warning(request, f"Label '{tag}' is empty!")
            return redirect(reverse('systems:view', args=[system.id]))
        items_per_page = Settings.load().items_per_page
        paginator = Paginator(incidents, items_per_page)
        page_number = request.GET.get("page")
        page_incidents = paginator.get_page(page_number)

        return render(request, 'system/incidents.html', {'system': system, 'incidents': page_incidents})
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
            return render(request, 'system/add.html', {'form': form})
        return render(request, 'system/add.html', {'form': form})
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
            return render(request, 'system/edit.html', {'form': form})
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

# def function(request):
#     if request.user.is_authenticated:
#         pass
#     else:
#         return redirect('home')
