from django.contrib.auth.models import User

from datetime import datetime

from config.models import Settings
from systems.models import System

from .models import Incident

def create_incident(system=None, log=None):
    incident = None
    email = False
    # case "System is down"
    if log is not None:
        system = System.objects.filter(ip=log.host).first()

        if system is None:
            print("System doesnt exist in database")
            return False

        incident = Incident.objects.create(
            system=system,
            tag=1,
            title= f" Possible anomaly found in {system.name}'s logs",
            message=f'At {incident.date}{incident.time} following log record was detected on {inciudent.system.name} {inciudent.system.ip}: \n' +
                    'Tags: ' + log.program + ' Message: ' + log.message + '\n',
            ip=system.ip)
        if system.email_notify:
            email = create_email(incident=incident, log=log)
            return email
        else:
            return False

    # case "Log anomaly detected"
    elif system is not None:
        Incident.objects.create(
            system=system,
            tag=0,
            title= f" System {system.name} {system.ip} is down.",
            message=f'System ip: {incident.ip} \nMessage: {incident.message} \nDate: {incident.date}{incident.time}',
            ip=system.ip)
        if system.email_notify:
            email = create_email(incident=incident)
            return email
        else:
            return False
    print("System or log must be provided")        
    return False

def create_email(incident=None, log=None):

    if incident is None:
        print("Incident must be provided")        
        return False

    notifications_mode = Settings.load().notifications_mode
    send_to = User.objects.values_list('email', flat=True).distinct()

    if notifications_mode != 0: 
        if incident.tag == 0 and (notifications_mode == 1 or notifications_mode == 3):
            return (
                    f'System {incident.system.name} is down',
                    incident.message,
                    'from@example.com',
                    send_to)
        elif incident.tag == 1 and (notifications_mode == 2 or notifications_mode == 3):
            return (
                    f"Abnormal record detected in {incident.system.name}'s logs",
                    incident.message,
                    'from@example.com',
                    send_to)
        else:
            print("Email disabled for this type of incidents")
            return False

    print("Email notifications disabled")
    return False
