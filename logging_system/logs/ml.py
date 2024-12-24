from django.shortcuts import render
from django.core.mail import send_mass_mail

from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, HDBSCAN
# from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.utils import Bunch
from sklearn_minisom import MiniSOM

import pandas as pd
import random
import joblib
import time
import os

from .models import Log
from .functions import zip_logs, get_logs
from config.models import Settings
from incidents.functions import create_incident

# from .functions import get_logs, send_anomaly_emails


# sklearn ML train function prototype
def train():

    settings = Settings.load()
    clf = settings.ml_classifier
    clf_tag = settings.get_ml_classifier_display()
    vec = settings.ml_vectorizer
    clusters = settings.ml_clusters

    data = get_logs(train=True)
    if data is None:
        return f"{clf_tag} Training: Not enough log data."

    df = pd.DataFrame()
    df['program'] = data.values('program')
    df['message'] = data.values('message')
    X = df['program'].astype(str) + " " + df['message'].astype(str)

    classifier = (
        KMeans(clusters) if clf == 0 else
        AgglomerativeClustering(n_clusters=clusters) if clf == 1 else
        DBSCAN(eps=0.8) if clf == 2 else 
        HDBSCAN() if clf == 3 else
        MiniSOM()
        )

    vectorizer = (
        TfidfVectorizer() if vec == 0 else
        CountVectorizer() 
    )

    pipeline = Pipeline([
        ('scaler', vectorizer),
        ('classifier', classifier)
    ])

    pipeline.fit(X)

    joblib.dump(pipeline, 'pipeline.joblib')

    return f"{clf_tag} Training: Success."


# sklearn ML classify function
def classify():
    settings = Settings.load()
    clf_tag = settings.get_ml_classifier_display()
    file = 'pipeline.joblib'

    if (os.path.exists(file)) is False:
        return f"{clf_tag} Classification: Pipeline file '{file}' doesn't exist."

    data = get_logs(train=False)
    if data is None:
        return f"{clf_tag} Classification: Not enough log data."

    df = pd.DataFrame()
    df['program'] = data.values('program')
    df['message'] = data.values('message')
    X = df['program'].astype(str) + " " + df['message'].astype(str)

    pipeline = joblib.load(file)
    labels = pipeline.fit_predict(X)
    
    if settings.ml_classifier in [2, 3]:
        labels = labels + 1

    emails, message = zip_logs(
        logs=data, 
        labels=labels, 
        anomaly_label = Settings.load().ml_anomaly_cluster
        )

    if emails is None:
        return message

    print(emails)
    if emails is not None and len(emails) != 0:
        send_mass_mail(emails)
    # send_anomaly_emails(data, debug=True)

    return f"{clf_tag} Classification: Success."

#######################################################################################################



#######################################################################################################

def remove_pipeline_file(file='pipeline'):
    file = file + '.joblib'
    if os.path.exists(file):
      os.remove(file)