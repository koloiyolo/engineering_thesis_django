from django.core.mail import send_mass_mail

from ping3 import ping
import plotly.graph_objs as go
from incidents.functions import create_incident
from .models import System, Ping
from config.models import Settings

def ping_systems(systems, debug=True):
    emails = []
    for system in systems:
        ip = system.ip
        response_time = ping(ip, unit='ms')
        print(f"{ip}, {response_time}")
        if response_time is not None:
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