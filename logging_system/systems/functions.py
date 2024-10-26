from django.core.mail import send_mass_mail

from ping3 import ping

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