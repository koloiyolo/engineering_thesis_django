from django import forms
import json
import numpy as np
from datetime import datetime
from django.contrib.auth.models import User

from .models import Settings

class SettingsPage(forms.ModelForm):

    ML_MODEL_CHOICES = [
        (0, 'K-Means'),
        (1, 'AHC'),
        (2, 'SOM'),
    ]
    BOOL_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    # Site settings
    site_name = forms.CharField(max_length="200",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Your site's name"}), label='Site name')
    maintenance_mode = forms.ChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect,label="Maintenance mode")
    contact_email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':"Admin email"}), label="Contact email")
    items_per_page = forms.IntegerField(widget=forms.NumberInput, label="Items per page")

    # Email settings
    email_host = forms.CharField(max_length="200",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"smtp.example.com"}), label='Your email hosting provider address', )
    email_port = forms.IntegerField(widget=forms.NumberInput, label = "Email hosting port")
    email_host_user = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':"user@example.com"}), label="Your email host address")
    email_host_password = forms.CharField(widget=forms.TextInput(attrs={'type':'password','class':'form-control', 'placeholder':"Your site's name"}), label="Emial host password")
    email_use_ssl = forms.ChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect,label="Use SSL protocol")
    email_from_address = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':"Use email host user if your email provider doesn't support aliases"}), label="Email from which messages will be sent")

    # ML Settings
    ml_model = forms.ChoiceField(choices=ML_MODEL_CHOICES, widget=forms.RadioSelect,label="Your Machine Learning model of choice: ")
    ml_train = forms.IntegerField(widget=forms.NumberInput, label = "Training data size")
    ml_classify = forms.IntegerField(widget=forms.NumberInput, label = "Classifying data size")


    class Meta:
        model = Settings
        fields = (
            "site_name",
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

        )