from django.contrib.auth.models import User
from .models import Ping
from website.models import Log
from systems.models import System


from ping3 import ping
import random
from django.core.mail import send_mass_mail

def send_anomaly_emails(data, debug = True):
    emails = []
    send_to = User.objects.values_list('email', flat=True).distinct()

    for obj in data:
        if obj.label == 6 or obj.label == 9:
            if debug:
                print(f'{obj.datetime} {obj.host} {obj.tags} {obj.message}')
            else:
                emails.append((
                    f'Abnormal record detected, label: {label}',
                    f'{obj.host} {obj.tags} {obj.message} {obj.datetime}',
                    'from@example.com',
                    send_to))

    if emails:       
        send_mass_mail(emails)

    return True