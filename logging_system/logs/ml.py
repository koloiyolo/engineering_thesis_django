from django.shortcuts import render
from django.core.mail import send_mass_mail

from sklearn.cluster import KMeans, AgglomerativeClustering
# from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import Bunch

from minisom import MiniSom

import numpy as np
import random
import joblib
import time
import os


from .models import Log
from config.models import Settings
from incidents.functions import create_incident
# from .functions import get_logs, send_anomaly_emails

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
        return None, "Logs dont exist"

    if labels is None:
        return None, "Labels dont exist"

    emails = []
    for log, label in zip(logs, labels):
            log.label = label
            log.save()
            if log.label == anomaly_label:
                email = create_incident(log=log)
                if email is not False:
                    emails.append(email)
    return emails, "Zipping complete"


# sklearn ML train function prototype
def train(model=KMeans(2, random_state=42), file_prefix='kmeans'):
    data = get_logs(Settings.load().ml_train)

    if data is not None:
        features = [obj.get_features() for obj in data]
        encoder = TfidfVectorizer()
        encoded_features = encoder.fit_transform(features).toarray()

        clf = model
        X = np.array(encoded_features)
        clf.fit(X)

        joblib.dump(clf, file_prefix + '.joblib')
        joblib.dump(encoder, file_prefix + '_encoder.joblib')

        return True

    else:
        return False

    return False


# sklearn ML classify function
def classify(file_prefix = 'kmeans'):
    emails = None
    clf_file = file_prefix + '.joblib'
    encoder_file = file_prefix + '_encoder.joblib'

    if (os.path.exists(clf_file) and os.path.exists(encoder_file)) is False:
        return False

    data = get_logs(Settings.load().ml_classify)
    if data is None:
        print("No data to classify")
        return True

    features = [obj.get_features() for obj in data]
    encoder = joblib.load(encoder_file)
    encoded_features = encoder.transform(features).toarray()
    X = np.array(encoded_features)
    clf = joblib.load(clf_file)
    labels = clf.predict(X)
    
    emails, message = zip_logs(
        logs=data, 
        labels=labels, 
        anomaly_label = Settings.load().ml_anomaly_cluster
        )

    print(emails)
    if emails is not None and len(emails) != 0:
        send_mass_mail(emails)
    # send_anomaly_emails(data, debug=True)

    return True

#######################################################################################################

# K-Means
def train_kmeans():
    clusters = Settings.load().ml_clusters
    return train(
        model = KMeans(clusters, random_state=42),
        file_prefix = 'kmeans'
    )

def classify_kmeans():
    return classify(
        file_prefix = 'kmeans'
    )

# AHC
def train_ahc():
    clusters = Settings.load().ml_clusters
    return train(
        model = AgglomerativeClustering(n_clusters=clusters),
        file_prefix = 'ahc'
    )

def classify_ahc():
    return classify(
        file_prefix = 'ahc'
    )

# SOM
def train_som():
    data = get_logs(Settings.load().ml_train)
    clusters = Settings.load().ml_clusters
    if data is None:
        return True

    file_prefix = 'som'
    features = [obj.get_features() for obj in data]
    encoder = TfidfVectorizer()
    encoded_features = encoder.fit_transform(features).toarray()
    input_len = encoded_features.shape[1]
    som = MiniSom(x=20, y=clusters, input_len=input_len, sigma=1, learning_rate=0.5)
    X = np.array(encoded_features)
    som.random_weights_init(encoded_features)
    som.train_random(encoded_features, 1000)
    joblib.dump(som, 'som.joblib')
    joblib.dump(encoder, 'som_encoder.joblib')
    
    return True

def classify_som():
    emails = []
    som_file = 'som.joblib'
    encoder_file = 'som_encoder.joblib'

    if os.path.exists(som_file) and os.path.exists(encoder_file):
        data = get_logs(Settings.load().ml_classify)
        if data is None or len(data) == 0:
            print("No data to classify")
            return True

        features = [log.get_features() for log in data]

        encoder = joblib.load(encoder_file)
        encoded_features = encoder.transform(features).toarray()

        som = joblib.load(som_file)

        labels = []
        for feat in encoded_features:
            winner = som.winner(feat)
            if winner == (0, 0):
                labels.append(0)  # Anomaly
            else:
                labels.append(1)  # Normal

        anomaly = Settings.load().ml_anomaly_cluster
        for log, label in zip(data, labels):
            log.label = label
            log.save()
            if log.label == anomaly:
                email = create_incident(log=log)
                if email is not False:
                    emails.append(email)

        if len(emails) != 0:
            send_mass_mail(emails)

        return True

    else:
        if train_som():
            classify_som()
            return True
        else:
            return False

    return False

#######################################################################################################
# 