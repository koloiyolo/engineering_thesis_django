from datetime import datetime

from config.models import Settings
from systems.models import System

from .models import Incident

def create_incident(ip=None, system=None, tag=0):
    # case "System is down"
    if tag is 0:
        incident = Incident.objects.create(
            system=system,
            tag=tag,
            message= f" System {system.name} {system.ip} is down.\n Failed to contact {system.name} after {Settings.objects.load().ping_retries} retries",
            ip=system.ip)
        send_email_notifications(incident=Incident)
        return True

    # case "Log anomaly detected"
    elif tag is 1:
        system = System.objects.filter(ip=ip)
        incident = Incident.objects.create(
            system=system,
            tag=tag,
            message= f" Possible anomaly found in {system.name}'s logs. \n Anomaly found {datetime.now()} \n IP Address {system.ip} \n System type: {system.system_type}",
            ip=system.ip)
        send_email_notifications(incident=Incident)
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
