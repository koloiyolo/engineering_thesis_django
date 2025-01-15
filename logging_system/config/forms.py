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
            "graph_interval",
            "notifications_mode",
            # "email_host",
            # "email_port",
            # "email_host_user",
            # "email_host_password",
            # "email_use_ssl",
            # "email_from_address",
            "ml_classifier",
            "ml_classifier_optional",
            "ml_vectorizer",
            "ml_classifier_parameters",
            "ml_classifier_parameters_optional",
            "ml_vectorizer_parameters",
            "on_model_change_reset",
            "ml_anomaly_cluster",
            "ml_train",
            "ml_classify"
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
            "notifications_mode": Select(attrs={
                'class': "form-control",
            }),
            # "email_host": TextInput(attrs={
            #     'class': "form-control",
            #     'label': 'Email hosting',
            #     'placeholder': 'smtp.example.com',                
            # }),
            # "email_port": NumberInput(attrs={
            #     'class': "form-control",
            #     'label': 'Email hosting port',
            #     'placeholder': '465',
            # }),
            # "email_use_ssl": Select(attrs={
            #     'class': "form-control",
            # }),
            # "email_host_user": EmailInput(attrs={
            #     'class': "form-control",
            #     'label': 'Email hosting user',
            #     'placeholder': 'user@example.com',                
            # }),
            # "email_host_password":  TextInput(attrs={
            #     'class': "form-control",
            #     'label': 'Email hosting user password',
            #     'type':'password',
            #     'placeholder': 'password',                
            # }),
            # "email_from_address": EmailInput(attrs={
            #     'class': "form-control",
            #     'label': 'Email address',
            #     'placeholder': 'user@example.com',                
            # }),
            "ml_classifier": Select(attrs={
                'class': "form-control",
            }),
            "ml_classifier_parameters": TextInput(attrs={
                'class': "form-control",
                'label': 'Classifier hyperparameters',
                'placeholder': "eg. {'n_clusters': 2, 'learning_rate': 0.01, 'eps': 0.8}",                
            }),
            "ml_classifier_optional": Select(attrs={
                'class': "form-control",
            }),
            "ml_classifier_parameters_optional": TextInput(attrs={
                'class': "form-control",
                'label': 'Classifier hyperparameters',
                'placeholder': "eg. {'n_clusters': 2, 'learning_rate': 0.01, 'eps': 0.8}",                
            }),
            "ml_vectorizer": Select(attrs={
                'class': "form-control",
            }),
            "ml_vectorizer_parameters": TextInput(attrs={
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
            "ml_classify": NumberInput(attrs={
                'class': "form-control",
                'placeholder': '2000'
            }),
        }
