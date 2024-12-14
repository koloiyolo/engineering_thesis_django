from django.core.mail import send_mass_mail
import re
from ping3 import ping
import plotly.graph_objs as go
from incidents.functions import create_incident
from .models import System, Ping
from config.models import Settings
from audit_log.models import AuditLog

def ping_systems(systems, debug=True):
    emails = []
    for system in systems:
        ip = system.ip
        response_time = ping(ip, unit='ms')
        print(f"{ip}, {response_time}")
        if response_time not in (False, None):
            system.last_ping = f'{int(response_time)} ms'
            system.d_count = 0
            Ping.objects.create(system=system, ping=response_time)
        else:
            system.last_ping = None
            system.d_count += 1
            if system.d_count == Settings.load().ping_retries:
                email = create_incident(system=system)
                if email is not False:
                    emails.append(email)
            Ping.objects.create(system=system, ping=None)
        
        system.save()
    if len(emails) != 0:
        send_mass_mail(emails)

    AuditLog.objects.create(user=None, text=f"All systems pinged.")
    return True

def get_ping_graph(system, height=300, width=900, range=144):
    pings = Ping.objects.filter(system=system).order_by('-id')[:range]
    n = 0
    timestamps = [n + i/12 for i,_ in enumerate(pings)]
    ping_values = [ping.ping for ping in pings][::-1]

    trace = go.Scatter(x=timestamps, y=ping_values, mode='lines', name='Ping', marker=dict(color='green'))
    layout = go.Layout(xaxis=dict(title='Time range (h)'), 
                       yaxis=dict(title='Ping (ms)'),
                       height=height,
                       width=width,)
    figure = go.Figure(data=[trace], layout=layout)
    plot_div = figure.to_html(full_html=False)

    return plot_div


def discover_systems(ip_range, system_type=None, prefix=""):
    systems = []
    match = re.search(r'^(([^.\\-]+)\.([^.\\-]+)\.([^.\\-]+)).*?([^.\\-]+)[-]([^.\\-]+)$', ip_range)
    
    # validate match 
    if not match:
        print(f"Invalid IP range format: {ip_range}")
        return False

    ip_prefix = match.group(1)
    try:
        first = int(match.group(5))
        last = int(match.group(6))
    except ValueError:
        print(f"Invalid IP range values in: {ip_range}")
        return False

    if first > last:
        print(f"Invalid range: start ({first}) is greater than end ({last})")
        return False

    for i in range(first, last+1):
        ip=f"{ip_prefix}.{i}"
        response_time = ping(ip, unit='ms')
        if response_time in (None, False):
            print(f"{ip}: host not found. Response: {response_time}")
        else:
            print(f"{ip}: host found")
            system = System.objects.create(
                name=f"{prefix}{ip}",
                ip=ip,
                system_type=system_type)
            systems.append(system)

    
    print(f"Added new systems: ")
    for system in systems:
        print(f"{system}")

    AuditLog.objects.create(user=None, text=f"New systems discovered prefix {prefix}.")
    return True