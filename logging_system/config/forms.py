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
            "email_host",
            "email_port",
            "email_host_user",
            "email_host_password",
            "email_use_ssl",
            "email_from_address",
            "ml_model",
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
            "items_per_page": NumberInput(attrs={
                'class': "form-control",
                'placeholder': '20'
            }),

            "email_host": TextInput(attrs={
                'class': "form-control",
                'label': 'Email hosting',
                'placeholder': 'smtp.example.com',                
            }),
            "email_port": NumberInput(attrs={
                'class': "form-control",
                'label': 'Email hosting port',
                'placeholder': '465',
            }),
            "email_use_ssl": Select(attrs={
                'class': "form-control",
            }),
            "email_host_user": EmailInput(attrs={
                'class': "form-control",
                'label': 'Email hosting user',
                'placeholder': 'user@example.com',                
            }),
            "email_host_password":  TextInput(attrs={
                'class': "form-control",
                'label': 'Email hosting user password',
                'type':'password',
                'placeholder': 'password',                
            }),
            "email_from_address": EmailInput(attrs={
                'class': "form-control",
                'label': 'Email address',
                'placeholder': 'user@example.com',                
            }),
            
            "ml_model": Select(attrs={
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