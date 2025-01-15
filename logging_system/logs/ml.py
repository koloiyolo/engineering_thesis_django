from django.shortcuts import render
from django.core.mail import send_mass_mail
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, HDBSCAN
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


# sklearn ML train function prototype
def train(clf=None, vec=None):

    settings = Settings.load()
    clf = clf if clf is not None else settings.ml_classifier
    clf_tag = settings.get_ml_classifier_display()
    vec = vec if vec is not None else settings.ml_vectorizer
    clf_params = ast.literal_eval(settings.ml_classifier_parameters) if settings.ml_classifier_parameters != "" else None
    vec_params = ast.literal_eval(settings.ml_vectorizer_parameters) if settings.ml_vectorizer_parameters != "" else None

    if settings.ml_classifier == 2 and settings.ml_classifier_optional is not None:
        return f"Training: AHC algorithm can't be used on first position on multistep pipeline."

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
    classifier = get_classifier(clf=settings.ml_classifier, clf_params=settings.ml_classifier_parameters)
    classifier_optional = None if settings.ml_classifier == None else get_classifier(
                                                                                    clf=settings.ml_classifier, 
                                                                                    clf_params=settings.ml_classifier_parameters_optional
                                                                                    )
                                                        

    pipe = [
        ('scaler', vectorizer),
        ('classifier', classifier)
    ] if classifier_optional is None else [
        ('scaler', vectorizer),
        ('classifier', classifier),
        ('classifier_optional', classifier_optional)
    ]

    pipeline = Pipeline(pipe)

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


def get_classifier(clf=1, clf_params=None):
    classifier = KMeans()
    try:
        if clf == 1:
            classifier = KMeans(**clf_params) if clf_params else KMeans(10)
        elif clf == 2: 
            classifier = AgglomerativeClustering(**clf_params) if clf_params else AgglomerativeClustering()
        elif clf == 3:  
            classifier = DBSCAN(**clf_params) if clf_params else DBSCAN(eps=0.8)
        elif clf == 4:  
            classifier = HDBSCAN(**clf_params) if clf_params else HDBSCAN()
        elif clf == 5:  
            classifier = MiniSOM(**clf_params) if clf_params else MiniSOM(x=5, y=5)
        else:
            classifier = None

    except Exception as e:
        print(f"Classifier hyperparameters error {e}")
        classifier = (
            KMeans(10) if clf == 1 else
            AgglomerativeClustering() if clf == 2 else
            DBSCAN(eps=0.8) if clf == 3 else 
            HDBSCAN() if clf == 4 else
            MiniSOM(5, 5) if clf == 5 else None
        )

    return classifier