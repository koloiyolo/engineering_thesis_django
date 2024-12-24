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
import ast

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
    clf_params = ast.literal_eval(settings.ml_classifier_parameters) if settings.ml_classifier_parameters != "" else None
    vec_params = ast.literal_eval(settings.ml_vectorizer_parameters) if settings.ml_vectorizer_parameters != "" else None


    data = get_logs(train=True)
    if data is None:
        return f"{clf_tag} Training: Not enough log data."

    df = pd.DataFrame()
    df['program'] = data.values('program')
    df['message'] = data.values('message')
    X = df['program'].astype(str) + " " + df['message'].astype(str)

    classifier = KMeans(10)
    vectorizer = TfidfVectorizer()

    try:
        if vec == 0:
            vectorizer = TfidfVectorizer(**vec_params) if vec_params else TfidfVectorizer()
        else: 
            vectorizer = CountVectorizer(**vec_params) if vec_params else CountVectorizer()

    except Exception as e:
        print(f"Vectorizer hyperparameters error {e}")
        vectorizer = (
            TfidfVectorizer() if vec == 0 else
            CountVectorizer() 
            )


    try:
        if clf == 0:
            classifier = KMeans(**clf_params) if clf_params else KMeans(10)
        elif clf == 1: 
            classifier = AgglomerativeClustering(**clf_params) if clf_params else AgglomerativeClustering()
        elif clf == 2:  
            classifier = DBSCAN(**clf_params) if clf_params else DBSCAN(eps=0.8)
        elif clf == 3:  
            classifier = HDBSCAN(**clf_params) if clf_params else HDBSCAN()
        else:  
            classifier = MiniSOM(**clf_params) if clf_params else MiniSOM(x=5, y=5)

    except Exception as e:
        print(f"Classifier hyperparameters error {e}")
        classifier = (
            KMeans(10) if clf == 0 else
            AgglomerativeClustering() if clf == 1 else
            DBSCAN(eps=0.8) if clf == 2 else 
            HDBSCAN() if clf == 3 else
            MiniSOM(5, 5)
            )

    pipeline = Pipeline([
        ('scaler', vectorizer),
        ('classifier', classifier)
    ])

    pipeline.fit(X)

    joblib.dump(pipeline, 'pipeline.joblib')

    return f"{classifier} Training: Success."


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