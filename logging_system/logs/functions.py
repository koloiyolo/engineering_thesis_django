from django.http import HttpResponse
import csv
import random
from .models import Log
from config.models import Settings
from incidents.functions import create_incident


# get logs from database
def get_logs(train=False):
    data = None
    settings = Settings.load()
    if train:
        _count = Log.objects.all().count()
        to_train = settings.ml_train
        if to_train > _count:
            offset = random.randint(0, (_count - to_train))
            data = Log.objects.all()[offset : offset + to_train]
        else:
            data = Log.objects.all()

        if data.count() < 2500:
            return None

        return data
    else:
        data = Log.objects.all().filter(label=None)[: settings.ml_cluster]
        if data.count() == 0:
            return None

    return data


# zips logs with labels and saves them to database
# creates incidents
# returns emails
def zip_logs(logs=None, labels=None, groups=None, anomaly_label=0):
    if logs is None:
        return None, "Classification: Logs dont exist"

    if labels is None:
        return None, "Classification: Labels dont exist"

    emails = []
    if groups:
        for log, label, group in zip(logs, labels, groups):
            if group:
                log.log_group = group

            if label == anomaly_label:
                log.label = 0
                log.save()
                email = create_incident(log=log)
                if email is not False:
                    emails.append(email)
            else:
                log.label = 1
                log.save()
    else:
        for log, label in zip(logs, labels):
            if label == anomaly_label:
                log.label = 0
                log.save()
                email = create_incident(log=log)
                if email is not False:
                    emails.append(email)
            else:
                log.label = 1
                log.save()

    return emails, "Zipping complete"


def export_csv(logs, count=None, labels=True, file_name="logs"):
    if labels:
        logs = logs.filter(label__isnull=False)

    if count is not None:
        logs = logs[:count]
    else:
        logs = logs

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={file_name}.csv"

    file = csv.writer(response)
    if labels:
        file.writerow(["datetime", "host", "program", "message", "label"])
        for log in logs:
            file.writerow([log.datetime, log.host, log.program, log.message, log.label])

    else:
        file.writerow(["datetime", "host", "program", "message"])
        for log in logs:
            file.writerow([log.datetime, log.host, log.program, log.message])

    return response
