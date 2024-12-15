from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q

from .functions import get_ping_graph, get_packet_loss
from logging_system.functions import pagination, logs_short_message

from .models import System, Ping
from incidents.models import Incident
from logs.models import Log
from locations.models import Location
from config.models import Settings
from .forms import SystemForm, DiscoverSystemsForm
from audit_log.models import AuditLog
from .tasks import discover_systems_task
# Create your views here.

def systems(request, location=None, system_type=None):
    if request.user.is_authenticated:

        systems = None
        q = request.GET.get('search', '')

        if location is not None:
            if q:
                systems = System.objects.filter(
                    Q(name__icontains=q) |
                    Q(ip__icontains=q) |
                    Q(service_type__icontains=q) |
                    Q(model__icontains=q) |
                    Q(location__name__icontains=q) |
                    Q(location__town__icontains=q) |
                    Q(location__address__icontains=q),
                    location=location
                ).order_by("id")
            else:
                systems = System.objects.filter(location=location).order_by("id")
        elif system_type is not None:
            if q:
                systems = System.objects.filter(
                    Q(name__icontains=q) |
                    Q(ip__icontains=q) |
                    Q(service_type__icontains=q) |
                    Q(model__icontains=q) |
                    Q(location__name__icontains=q) |
                    Q(location__town__icontains=q) |
                    Q(location__address__icontains=q),
                    system_type=system_type
                ).order_by("id")
            else:
                systems = System.objects.filter(system_type=system_type).order_by("id")
        else:
            if q:
                systems = System.objects.filter(
                    Q(name__icontains=q) |
                    Q(ip__icontains=q) |
                    Q(service_type__icontains=q) |
                    Q(model__icontains=q) |
                    Q(location__name__icontains=q) |
                    Q(location__town__icontains=q) |
                    Q(location__address__icontains=q)
                ).order_by("id")
            else:
                systems = System.objects.order_by("id")

        # update system last_log
        for system in systems:
            last_log = Log.objects.filter(host= system.ip).last()
            if last_log is not None:
                system.last_log = last_log.datetime
                system.save()
        
        page = pagination(systems, request.GET.get("page"))

        locations = Location.objects.all()

        # calculate packet loss
        for system in page:
            system.loss = get_packet_loss(system)

        data = {
            'systems': page,
            'locations': locations
        }
        return render(request, 'system/list.html', data)
    else:
        return redirect('home')



def system(request, pk):
    if request.user.is_authenticated:
        system = System.objects.get(id=pk)
        system.graph = get_ping_graph(system)

        system.loss = get_packet_loss(system)

        last_log = Log.objects.filter(host=system.ip).last()
        if last_log is not None:
            system.last_log = last_log.datetime
            system.save()

        system.graph = get_ping_graph(system)

        # logs
        logs = Log.objects.filter(host=system.ip).order_by("-id")[:10]
        clusters = Log.objects.filter(label__isnull=False).values_list('label', flat=True).distinct()
        logs = logs_short_message(logs)
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

def logs(request, pk, label=None):
    if request.user.is_authenticated:
        system = System.objects.get(id=pk)

        logs = None
        q = request.GET.get('search', '')

        if label:
            if q:
                logs = logs.objects.filter(
                    Q(host__icontains=q) |
                    Q(program__icontains=q) |
                    Q(message__icontains=q),
                    host=system.ip,
                    label=label
                ).order_by("-id")
            else:
                logs = Log.objects.filter(host=system.ip, label=label).order_by('-id')
        else:
            if q:
                logs = logs.objects.filter(
                    Q(host__icontains=q) |
                    Q(program__icontains=q) |
                    Q(message__icontains=q),
                    host=system.ip
                ).order_by("-id")
            else:
                logs = Log.objects.filter(host=system.ip).order_by('-id')

        if not logs.exists():
            messages.warning(request, f"Label '{label}' is empty!")
            return redirect('logs')
        
        page = pagination(logs, request.GET.get("page"))
        clusters = Log.objects.filter(label__isnull=False).values_list('label', flat=True).distinct()

        page = logs_short_message(page)

        hosts = Log.objects.all().values_list('host', flat=True).distinct()

        systems = []
        for host in hosts:
            systems.append(System.objects.filter(ip=host).first())

        data = {
            'system': system,
            'systems': systems,
            'logs': page,
            'clusters': clusters}
        return render(request, 'misc/logs.html', data)
        pass
    else:
        return redirect('home')


def incidents(request, pk):
    if request.user.is_authenticated:
        system = System.objects.get(id=pk)

        incidents = None
        q = request.GET.get('search', '')
        if q:
            incidents = incidents.filter(
                Q(message__icontains=q) |
                Q(ip__icontains=q) |
                Q(title__icontains=q) |
                Q(tag__icontains=q),
                system=system
            ).order_by("-id")
        else:
            incidents = Incident.objects.filter(system=system).order_by("-id")   

        if not incidents.exists():
            messages.warning(request, f"There are no incidents for {system.name}")
            return redirect(reverse('systems:view', args=[system.id]))
        
        page = pagination(incidents, request.GET.get("page"))

        systems = System.objects.filter(id__in=Incident.objects.values_list('system', flat=True).distinct())
        return render(request, 'incident/list.html', {
            'system': system,
            'systems': systems,
            'incidents': page})
    else:
        return redirect('home')

def tag_incidents(request, pk, tag):
    if request.user.is_authenticated:
        system = System.objects.get(id=pk)

        incidents = Incident.objects.filter(system=system, tag=tag).order_by("-id")
        if q:
            incidents = incidents.filter(
                Q(message__icontains=q) |
                Q(ip__icontains=q) |
                Q(title__icontains=q)
            )
        if not incidents.exists():
            messages.warning(request, f"Label '{tag}' is empty!")
            return redirect(reverse('systems:view', args=[system.id]))
        
        page = pagination(incidents, request.GET.get("page"))
        systems = System.objects.filter(id__in=Incident.objects.values_list('system', flat=True).distinct())
        return render(request, 'incident/list.html', {
            'system': system,
            'systems': systems,
            'incidents': page})
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
                AuditLog.objects.create(user=request.user, text=f"{request.user} created system {add_record} successfully.")
                messages.success(request, "System added successfully")
                return redirect('systems:list')
        else:
            return render(request, 'system/add.html', {'form': form})
        return render(request, 'system/add.html', {'form': form})
    else:
        return redirect('home')

def discover(request):
    if request.user.is_authenticated:
        form = DiscoverSystemsForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():

                ip_range = form.cleaned_data.get("ip_range")
                system_type = form.cleaned_data.get("system_type")
                prefix = form.cleaned_data.get("prefix") if form.cleaned_data.get("prefix") else ""
                discover_systems_task.delay(ip_range, system_type=system_type, prefix=prefix)
                AuditLog.objects.create(user=request.user, text=f"{request.user} scheluded discovery task on {ip_range} ip range.")
                messages.success(request, "System discovery sheluded")
                return redirect('systems:list')

        else:
            return render(request, 'system/discover.html', {'form': form})
        return render(request, 'system/discover.html', {'form': form})


    else:
        return redirect('home')



def edit(request, pk):
    if request.user.is_authenticated:
        update_it = System.objects.get(id=pk)
        form = SystemForm(request.POST or None, instance=update_it)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(user=request.user, text=f"{request.user} updated system {update_it} successfully.")
            messages.success(request, "System updated successfully")
            return redirect('systems:list')
        else:
            return render(request, 'system/edit.html', {'form': form})
    else:
        return redirect('home')

def remove(request, pk):
    if request.user.is_authenticated:
        delete_it = System.objects.get(id=pk)
        AuditLog.objects.create(user=request.user, text=f"{request.user} removed system {delete_it} successfully.")
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
