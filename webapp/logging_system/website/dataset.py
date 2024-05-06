from django.shortcuts import render

from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import Bunch

import numpy as np
import random

from .models import Log

def create_dataset(dataset_size=1000, n_clusters=10):

    logs = Log.objects.all()
    ids = random.sample(range(0, len(logs)), dataset_size)

    data = []
    for id in ids:
        data.append(Log.objects.get(id=id))

    features = [[obj.datetime, obj.message, obj.host, obj.tags] for obj in data]
    encoder = OneHotEncoder()
    encoded_features = encoder.fit_transform(np.array(features).reshape(-1, 1))
    encoded_features = encoded_features.toarray()
    X = np.array(encoded_features)

    kmeans = KMeans(n_clusters)
    kmeans.fit(X)
    labels = kmeans.labels_
    data = np.array(features)
    dataset = Bunch(data = data, target=np.array(labels))
    return dataset

