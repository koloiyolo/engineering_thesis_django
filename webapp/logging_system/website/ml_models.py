from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import Bunch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

import numpy as np
import joblib

from .models import Dataset


def create_model(name, dataset_id, model_type, args):

    dataset = Dataset.objects.get(pk=dataset_id)
    dataset_data = dataset.get_dataset()
    data = dataset_data['data']
    target = dataset_data['target']

    encoder = OneHotEncoder()
    encoded_data = encoder.fit_transform(np.array(data).reshape(-1, 1))
    encoded_data = encoded_data.toarray()
    
    X_train, X_test, y_train, y_test = train_test_split(encoded_data, target, test_size=0.3, random_state=42)

    classifier = None

    if model_type == 'knn':
        classifier = KNeighborsClassifier()
    elif model_type == 'rf':
        classifier = RandomForestClassifier()
    elif model_type == 'nb':
        classifier = GaussianNB()
    elif model_type == 'nn':
        classifier = MLPClassifier()
    elif model_type == 'svm':
        classifier = SVC()

    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    model = joblib.dump(classifier, "{name}.pkl")
    return model, accuracy



