from datetime import datetime

from config.models import Settings
from systems.models import System

from .models import Incident

def create_incident(ip=None, system=None, tag=0):
    # case "System is down"
    if tag is 0:
        Incident.objects.create(
            system=system,
            tag=tag,
            message= f" System {system.name} is down.\n Failed to contact {system.name} after {Settings.load().ping_retries} retries \n \n Incident date: {datetime.now()} \n IP Address: {system.ip} \n System type: {system.system_type}",
            ip=system.ip)
        if system.email_notify:
            # send_email_notifications(incident=incident)
            return True
        else:
            return True

    # case "Log anomaly detected"
    elif tag is 1:
        system = System.objects.filter(ip=ip)
        incident = Incident.objects.create(
            system=system,
            tag=tag,
            message= f" Possible anomaly found in {system.name}'s logs. \n\n Anomaly date: {datetime.now()} \n IP Address: {system.ip} \n System type: {system.system_type}",
            ip=system.ip)
        if system.email_notify:
            # send_email_notifications(incident=incident)
            return True
        else:
            return True
            
    return False

def send_email_notifications(incident=None):
    send_email_notifications = Settings.load().send_email_notifications
    if send_email_notifications:
        notifications_mode = Settings.load().notifications_mode 
        if incident.tag is 0 and (notifications_mode is 1 or 3):

            return True
        elif incident.tag is 1 and (notifications_mode is 2 or 3):

            return True
        else:
            print("Email disabled for this type of incidents")
            return True
        return False
    else:
        print("Email notifications disabled")
        return True
    return False
