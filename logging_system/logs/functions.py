from django.http import HttpResponse
import csv

from .models import Log
from config.models import Settings
from incidents.functions import create_incident



# get logs from database
def get_logs(count):
    data = None
    _count = Log.objects.all().count()
    if count > _count:
        offset = random.randint(0, (_count - count))
        data = Log.objects.all()[offset:offset + count]
    else:
        data = Log.objects.all()
    
    data = Log.objects.all().filter(label=None)[:2500]

    if data.count() == 0:
        data = None
        return data

    return data

# zips logs with labels and saves them to database
# creates incidents
# returns emails
def zip_logs(logs=None, labels=None, anomaly_label=0):

    if logs is None:
        return None, "Classification: Logs dont exist"

    if labels is None:
        return None, "Classification: Labels dont exist"

    emails = []
    for log, label in zip(logs, labels):
            log.label = label
            log.save()
            if log.label == anomaly_label:
                email = create_incident(log=log)
                if email is not False:
                    emails.append(email)
    return emails, "Zipping complete"


def export_csv(logs, count=None, labels=True, file_name="logs"):

    if labels:
        logs = logs.filter(label__isnull=False)
    
    if count is not None:
        logs = logs[:count]
    else: 
        logs = logs

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f"attachment; filename={file_name}.csv"

    file = csv.writer(response)
    if labels:
        file.writerow(['datetime', 'host', 'program', 'message', 'label'])
        for log in logs:
            file.writerow([log.datetime, log.host, log.program, log.message, log.label])

    else: 
        file.writerow(['datetime', 'host', 'program', 'message'])
        for log in logs:
            file.writerow([log.datetime, log.host, log.program, log.message])

    return response
