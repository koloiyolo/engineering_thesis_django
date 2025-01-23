from django import forms
from django.forms import TextInput, EmailInput, NumberInput, Select
import json
import numpy as np
from datetime import datetime
from django.contrib.auth.models import User

from .models import Settings

class SettingsPage(forms.ModelForm):

    class Meta:
        model = Settings
        fields = [
            "maintenance_mode",
            "contact_email",
            "items_per_page",
            "ping_retries",
            "ping_interval",
            "graph_interval",
            "notifications_mode",
            "s1_clusterer",
            "s2_clusterer",
            "s1_vectorizer",
            "s2_vectorizer",
            "s1_clusterer_parameters",
            "s2_clusterer_parameters",
            "s1_vectorizer_parameters",
            "s2_vectorizer_parameters",
            "on_model_change_reset",
            "ml_anomaly_cluster",
            "ml_train",
            "ml_train_interval",
            "ml_classify",
            "ml_classify_interval"
        ]
        widgets = {
            "maintenance_mode": Select(attrs={
                'class': "form-control",
            }),
            "contact_email": EmailInput(attrs={
                'class': "form-control",
                'label': 'Contact email',
                'placeholder': 'admin@example.com',
            }),
            "items_per_page": Select(attrs={
                'class': "form-control"
            }),
            "ping_retries": NumberInput(attrs={
                'class': "form-control",
                'placeholder': '20'
            }),
            "graph_interval": Select(attrs={
                'class': "form-control",
                'placeholder': 'Interval in hours, eg. 12'
            }),
            "ping_interval": Select(attrs={
                'class': "form-control"
            }),
            "notifications_mode": Select(attrs={
                'class': "form-control",
            }),
            "s1_clusterer": Select(attrs={
                'class': "form-control",
            }),
            "s1_clusterer_parameters": TextInput(attrs={
                'class': "form-control",
                'label': 'Classifier hyperparameters',
                'placeholder': "eg. {'n_clusters': 2, 'learning_rate': 0.01, 'eps': 0.8}",                
            }),
            "s2_clusterer": Select(attrs={
                'class': "form-control",
            }),
            "s2_clusterer_parameters": TextInput(attrs={
                'class': "form-control",
                'label': 'Classifier hyperparameters',
                'placeholder': "eg. {'n_clusters': 2, 'learning_rate': 0.01, 'eps': 0.8}",                
            }),
            "s1_vectorizer": Select(attrs={
                'class': "form-control",
            }),
            "s1_vectorizer_parameters": TextInput(attrs={
                'class': "form-control",
                'label': 'Classifier hyperparameters',
                'placeholder': "eg. {lowercase=True, preprocessor=None}",                
            }),
            "s2_vectorizer": Select(attrs={
                'class': "form-control",
            }),
            "s2_vectorizer_parameters": TextInput(attrs={
                'class': "form-control",
                'label': 'Classifier hyperparameters',
                'placeholder': "eg. {lowercase=True, preprocessor=None}",                
            }),
            "on_model_change_reset": Select(attrs={
                'class': "form-control",
            }),
            "ml_anomaly_cluster": Select(attrs={
                'class': "form-control",
            }),
            "ml_train": NumberInput(attrs={
                'class': "form-control",
                'placeholder': '10000'
            }),
            "ml_train_interval": Select(attrs={
                'class': "form-control"
            }),
            "ml_classify": NumberInput(attrs={
                'class': "form-control",
                'placeholder': '2000'
            }),
            "ml_classify_interval": Select(attrs={
                'class': "form-control"
            }),
        }
