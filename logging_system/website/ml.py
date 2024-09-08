from django.shortcuts import render

from sklearn.cluster import KMeans, AgglomerativeClustering
# from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import Bunch

from minisom import MiniSom

import numpy as np
import time
import joblib
import os

from .functions import get_logs

from .models import Log
from config.models import Settings
# from .functions import get_logs, send_anomaly_emails


# sklearn ML train function prototype
def train(model=KMeans(2, random_state=42), file_prefix='kmeans'):
    data = get_logs(Settings.load().ml_train)
    if data is not None:
        features = [obj.get_features() for obj in data]
        encoder = TfidfVectorizer()
        encoded_features = encoder.fit_transform(features).toarray()

        clf = KMeans(10, random_state=42)
        X = np.array(encoded_features)
        clf.fit(X)

        joblib.dump(clf, file_prefix + '.joblib')
        joblib.dump(encoder, file_prefix + '_encoder.joblib')

        return True

    else:
        return True

    return False

# sklearn ML classify function prototype
def classify(file_prefix = 'kmeans'):
    clf_file = file_prefix + '.joblib'
    encoder_file = file_prefix + '_encoder.joblib'
    if os.path.exists(clf_file) and os.path.exists(encoder_file):
        data = get_logs(Settings.load().ml_classify)
        if data is None:
            print("No data to classify")
            return True

        features = [obj.get_features() for obj in data]

        encoder = joblib.load(encoder_file)
        encoded_features = encoder.transform(features).toarray()
        X = np.array(encoded_features)

        clf = joblib.load(clf_file)
        clf.fit(X)
        labels = clf.labels_
        for log, label in zip(data, labels):
            log.label = label
            log.save()

        # send_anomaly_emails(data, debug=True)

        return True
    else:
        return True
    return False

#######################################################################################################

# K-Means
def train_kmeans():
    return train(
        model = KMeans(2, random_state=42),
        file_prefix = 'kmeans'
    )

def classify_kmeans():
    return classify(
        file_prefix = 'kmeans'
    )

# AHC
def train_ahc():
    return train(
        model = AgglomerativeClustering(n_clusters=2),
        file_prefix = 'ahc'
    )

def classify_ahc():
    return classify(
        file_prefix = 'ahc'
    )

# SOM
def train_som():
    data = get_logs(Settings.load().ml_train)
    if data is not None:
        file_prefix = 'som'
        features = [obj.get_features() for obj in data]
        encoder = TfidfVectorizer()
        encoded_features = encoder.fit_transform(features).toarray()
        input_len = encoded_features.shape[1]

        som = MiniSom(x=20, y=2, input_len=input_len, sigma=1, learning_rate=0.5)
        X = np.array(encoded_features)
        som.random_weights_init(encoded_features)
        som.train_random(encoded_features, 1000)

        joblib.dump(som, 'som.joblib')
        joblib.dump(encoder, 'som_encoder.joblib')

        return True

    else:
        return False

    return False

def classify_som():
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
                labels.append(0)  # Normal
            else:
                labels.append(1)  # Anomaly


        for log, label in zip(data, labels):
            log.label = label
            log.save()

        send_anomaly_emails(data, debug=True)

        return True

    else:
        if train_som():
            classify_som()
            return True
        else:
            return False

    return False