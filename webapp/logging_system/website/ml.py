from django.shortcuts import render

from sklearn.cluster import KMeans, AgglomerativeClustering
# from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.utils import Bunch

import numpy as np
import random
import time
import joblib
import os

from django.core.mail import send_mail

from .models import Log

def train():
    count = Log.objects.count()
    if count > 20000:
        data = None
        offset = None
        if count > 100000:
            offset = random.randint(0, (count - 100000))
            data = Log.objects.all()[offset:offset + 100000]

        elif count > 50000:
            offset = random.randint(0, (count - 50000))
            data = Log.objects.all()[offset:offset + 50000]
            
        else:
            offset = random.randint(0, (count - 20000))
            data = Log.objects.all()[offset:offset + 20000]
        
        features = [obj.get_features() for obj in data]
        encoder = TfidfVectorizer()
        encoder.fit(features)
        encoded_features = encoder.transform(features)
        encoded_features = encoded_features.toarray()


        clf = KMeans(10, random_state=42)
        X = np.array(encoded_features)
        clf.fit(X)

        joblib.dump(clf, 'kmeans.joblib')
        joblib.dump(encoder, 'encoder.joblib')

        return True

    else:
        return True

    pass

def classify():
    if os.path.exists("kmeans.joblib") and os.path.exists("encoder.joblib"):
        data = Log.objects.all().filter(label=None)[:2500]

        features = [obj.get_features() for obj in data]

        encoder = joblib.load("encoder.joblib")

        encoded_features = encoder.fit_transform(features)
        encoded_features = encoded_features.toarray()

        X = np.array(encoded_features)
        clf = joblib.load("kmeans.joblib")
        clf.fit(X)
        labels = clf.labels_

        for log, label in zip(data, labels):
            log.label = label
            log.save()
            if label == 6 or label == 9:

                # !!! Change to send_email() !!!

                # send_mail(
                #     f'Abnormal record detected, label: {label}',
                #     f'{log.host} {log.tags} {log.message} {log.datetime}',
                #     'from@example.com',
                #     ["to@example.com"],
                #     fail_silently=False,

                # )

                print(f'{log.datetime} {log.host} {log.tags} {log.message}')

        return True
    else:
        return True
    return False