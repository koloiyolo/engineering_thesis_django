from django.shortcuts import render

from sklearn.cluster import KMeans, AgglomerativeClustering, MeanShift, BisectingKMeans
# from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.utils import Bunch

import numpy as np
import random
import time

from .models import Log
from .ml import train

def classify(model_type='kmeans', size=10000, offset=0):
    train()
    data = Log.objects.all().filter(label=None)[:size]

    features = [obj.get_features() for obj in data]

    # OneHotEncoder
    # encoder = OneHotEncoder()
    # encoded_features = encoder.fit_transform(np.array(features).reshape(-1, 1))
    # encoded_features = encoded_features.toarray()

    encoder = TfidfVectorizer()
    encoded_features = encoder.fit_transform(features)
    encoded_features = encoded_features.toarray()
    X = np.array(encoded_features)

    clf = None
    if model_type == 'kmeans':
        clf = KMeans(10)
    elif model_type == 'bkmeans':
        classifier = BisectingKMeans()
    elif model_type == 'ahc':
        clf =  AgglomerativeClustering(linkage='single')
    elif model_type == 'ms':
        clf = MeanShift()
    elif model_type == 'ward':
        clf = AgglomerativeClustering()

    start_time = time.time()
    clf.fit(X)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{model_type} Execution time: {format(execution_time)} seconds")
    labels = clf.labels_

    for obj, label in zip(data, labels):
        obj.label = label
        obj.save()

    classification = Bunch(data = np.array(features), target=np.array(labels))

    # classification = [[] for _ in range(len(np.unique(labels)))]
    # for obj, label in zip(data, np.array(labels)):
    #     classification[label].append(obj)

    # print(classification)

    return classification

