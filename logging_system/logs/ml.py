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



# sklearn ML train function prototype
def train(cl=None, vec=None):

    settings = Settings.load()
    cl = cl if cl is not None else settings.s1_clusterer
    vec = vec if vec is not None else settings.s1_vectorizer

    if cl is None or vec is None:
        return f"Training: Skipping. No algorithm selected"
    
    cl_tag = settings.get_s1_clusterer_display()
    cl_params = None if settings.s1_clusterer_parameters == "" else ast.literal_eval(settings.s1_clusterer_parameters)
    vec_params = None if settings.s1_vectorizer_parameters == "" else ast.literal_eval(settings.s1_vectorizer_parameters)


    data = get_logs(train=True)
    if data is None:
        return f"{cl_tag} Training: Not enough log data."

    df = pd.DataFrame()
    df['program'] = data.values('program')
    df['host'] = data.values('host')
    X = df['host'].astype(str) + " " + df['program'].astype(str)

    vectorizer = get_preprocessor(vec=vec, vec_params=vec_params)
    clusterer = get_clusterer(cl=settings.s1_clusterer, cl_params=cl_params)
                                                        

    step1 = [
        ('vectorizer', vectorizer),
        ('clusterer', clusterer)
    ]

    pipeline = Pipeline(step1)

    pipeline.fit(X)

    joblib.dump(pipeline, 'step1.joblib')

    return f"{clusterer} Training: Success."

# sklearn ML cluster function
def cluster():
    settings = Settings.load()
    cl = settings.s2_clusterer
    cl1_tag = settings.get_s2_clusterer_display()
    cl2_tag = settings.get_s2_clusterer_display()
    vec = settings.s2_vectorizer
    cl_params = None if settings.s2_clusterer_parameters == "" else ast.literal_eval(settings.s2_clusterer_parameters)
    vec_params = None if settings.s2_vectorizer_parameters == "" else ast.literal_eval(settings.s2_vectorizer_parameters) 
    labels = None

    file = 'step1.joblib'

    data = get_logs(train=False)
    if data is None:
        return f"{cl2_tag} Classification: Not enough log data."

    
    df = pd.DataFrame()
    df['message'] = data.values('message')
    
    step2 = Pipeline([
        ('vectorizer', get_preprocessor(vec=vec, vec_params=vec_params)),
        ('clusterer', get_clusterer(cl=cl, cl_params=cl_params))
    ])

    if settings.s1_clusterer and settings.s1_vectorizer:
        step1 = None
        if (os.path.exists(file)):
            step1 = joblib.load(file)
        else: 
            step1 = Pipeline([
                ('vectorizer', get_preprocessor(vec=settings.s1_vectorizer, vec_params=settings.s1_vectorizer_parameters)),
                ('clusterer', get_clusterer(cl=settings.s1_clusterer, cl_params=settings.s1_clusterer_parameters))
            ])

        df['host'] = data.values('host')
        df['program'] = data.values('program')

        # Step 1
        df['group'] = grouping(data=df, pipeline=step1)

        # Step 2
        labels = outlier_detection(data=df, pipeline=step2)
    else:
        labels = step2.fit_predict(df['message'].astype(str))

    # DBSCAN / HDBSCAN correction
    if cl in [2, 3]:
        labels = labels + 1

    emails, message = zip_logs(
        logs=data,
        groups = df.get('group', None),
        labels=labels, 
        anomaly_label = Settings.load().ml_anomaly_cluster
        )

    if emails is None:
        return message

    print(emails)
    if emails is not None and len(emails) != 0:
        send_mass_mail(emails)
    # send_anomaly_emails(data, debug=True)

    return f"Step 1 Grouping: {cl1_tag} Step 2 Anomaly Detection: {cl2_tag}, Status: Success."

#######################################################################################################



#######################################################################################################

def remove_pipeline_file(file='step1'):
    file = file + '.joblib'
    if os.path.exists(file):
      os.remove(file)


def get_clusterer(cl=1, cl_params=None):
    clusterer = KMeans()
    try:
        if cl == 1:
            clusterer = KMeans(**cl_params) if cl_params else KMeans(10)
        elif cl == 2: 
            clusterer = AgglomerativeClustering(**cl_params) if cl_params else AgglomerativeClustering()
        elif cl == 3:  
            clusterer = DBSCAN(**cl_params) if cl_params else DBSCAN(eps=0.8)
        elif cl == 4:  
            clusterer = HDBSCAN(**cl_params) if cl_params else HDBSCAN()
        elif cl == 5:  
            clusterer = MiniSOM(**cl_params) if cl_params else MiniSOM(x=5, y=5)
        else:
            clusterer = None

    except Exception as e:
        print(f"Classifier hyperparameters error {e}")
        clusterer = (
            KMeans(10) if cl == 1 else
            AgglomerativeClustering() if cl == 2 else
            DBSCAN(eps=0.8) if cl == 3 else 
            HDBSCAN() if cl == 4 else
            MiniSOM(5, 5) if cl == 5 else None
        )

    return clusterer

def get_preprocessor(vec=1, vec_params=None):
    vectorizer = CountVectorizer()
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
    return vectorizer

def grouping(data=None, pipeline = None):
    X = data['host'].astype(str) + " " + data['program'].astype(str)
    y = pipeline.fit_predict(X)

    return y

def outlier_detection(data=None, pipeline = None):
    try:
        grouped_data = data.groupby('group')

        for _, group_data in grouped_data:
            X = group_data['message'].astype(str)
            group_data['cluster'] = pipeline.fit_predict(X)
            data.loc[group_data.index, 'cluster'] = group_data['cluster']
    except Exception as e:
        print(f"Outlier Detection Exception: {e}")
        return None

    return data['cluster']