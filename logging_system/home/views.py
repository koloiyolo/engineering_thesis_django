from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from ping3 import ping
from requests import get
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from config.models import Settings
from systems.models import System
from incidents.models import Incident
from logs.models import Log
from .forms import SignUpForm
from .functions import get_labels_graph, get_uptime_graph
from audit_log.models import AuditLog

# docker compose health check
def health_check(request):
    return JsonResponse({'status': 'ok'})

# Create your views here.

@login_required
def home(request):
    
    response = None
    ip = None

    incidents = Incident.objects.all().order_by("-id")[:Settings.load().items_per_page]

    try:
        response = f"{ping('8.8.8.8', unit='ms'):.3} ms"
        ip = get('https://api.ipify.org').content.decode('utf8')
    except:
        response = None
        ip = None
        
    # systems_d = System.objects.filter(last_ping=None)
    # for system in systems_d:
    #     system.graph = get_ping_graph(system, width=490)


    # labels_graph = get_labels_graph()
    # uptime_graph = get_uptime_graph()

    class Statistics:
        pass

    statistics = Statistics()
    
    # Incidents
    statistics.incident_count = Incident.objects.count()
    statistics.incident_resolved_count = Incident.objects.filter(user__isnull=False).count()
    
    try:
        statistics.incident_resolved_ratio = round(statistics.incident_resolved_count / statistics.incident_count * 100)
    except ZeroDivisionError:
         statistics.incident_resolved_ratio = 0

    statistics.incident_tag0_count = Incident.objects.filter(tag=0).count()
    statistics.incident_tag1_count = Incident.objects.filter(tag=1).count()
    # statistics.incident_tag0_resolved_count = Incident.objects.filter(tag=0, user__isnull=False).count()
    # statistics.incident_tag1_resolved_count = Incident.objects.filter(tag=1, user__isnull=False).count()
    statistics.incident_tag0_unresolved_count = Incident.objects.filter(tag=0, user__isnull=True).count()
    statistics.incident_tag1_unresolved_count = Incident.objects.filter(tag=1, user__isnull=True).count()

    try:
        statistics.incident_tag0_ratio = round(statistics.incident_tag0_unresolved_count /                                            100 * statistics.incident_tag0_count)
    except ZeroDivisionError:
         statistics.incident_tag0_ratio = 0

    try:
        statistics.incident_tag1_ratio = round(statistics.incident_tag1_unresolved_count / 
                                           statistics.incident_tag1_count * 100)
    except ZeroDivisionError:
         statistics.incident_tag1_ratio = 0

    # Log
    statistics.log_count = Log.objects.count()
    statistics.log_anomaly_count = Log.objects.filter(label=0).count()
    statistics.log_anomaly_ratio = round(statistics.log_anomaly_count/statistics.log_count * 100)

    statistics.log_devices_anomaly = Log.objects.filter(label=0).values('host').annotate(count=Count('host')).order_by('-count')

    # Systems
    statistics.system_count = System.objects.count()
    statistics.system_down_count = System.objects.filter(d_count__gt=0).count()
    statistics.system_down_ratio = round(statistics.system_down_count / statistics.system_count * 100)

    statistics.system_systems_down = System.objects.filter(d_count__gt=0).order_by('d_count')[:3]
    
    data = {'ip': ip,
            'ping': response,
            'incidents': incidents,
            'statistics': statistics,
            # 'logs': logs,
            # 'labels_graph': labels_graph,
            # 'uptime_graph': uptime_graph
            }

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
            AuditLog.objects.create(user=user, text=f"{user} created account successfuly.")
            messages.success(request, "You have successfuly created an account!")
            return redirect('home')
        pass
    else:
        form = SignUpForm()
        return render(request, 'registration/register.html', {'form': form})
        
    return render(request, 'registration/register.html', {'form': form})
