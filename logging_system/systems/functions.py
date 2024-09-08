from ping3 import ping

from incidents.functions import create_incident

from .models import System, Ping
from config.models import Settings

def ping_systems(systems, debug=True):

    for system in systems:
        ip = system.ip
        response_time = ping(ip, unit='ms')
        print(f"{ip}, {response_time}")
        if response_time is not None:
            system.last_ping = f'{int(response_time)} ms'
            system.d_count = 0
        else:
            system.last_ping = None
            system.d_count = system.d_count + 1
            if system.d_count == Settings.objects.load().ping_retries and system.email_notify:
                create_incident(system=system, tag=0)
        
        system.save()
        Ping.objects.create(system=system, ping=response_time)

    return True