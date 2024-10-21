from django import forms
from django.forms import TextInput, NumberInput, Select

from .models import System, Log

class SystemForm(forms.ModelForm):

    class Meta:
        model = System
        fields = [
            "name",
            "ip",
            "system_type",
            "to_ping",
            "email_notify",
            "port",
            "model",
            "location"
        ]
        widgets = {
            "name": TextInput(attrs={
                'class': "form-control",
                'label': "System's name",
                'placeholder': "Your system's name",                
            }),
            "ip":  TextInput(attrs={
                'class': "form-control",
                'label': "IP address",
                'placeholder': "Your system's ip address",                
            }),
            "system_type": Select(attrs={
                'class': "form-control",
            }),
            "to_ping": Select(attrs={
                'class': "form-control",
            }),
            "email_notify": Select(attrs={
                'class': "form-control",
            }),
            "port": NumberInput(attrs={
                'class': "form-control",
                'placeholder': ''
            }),
            "model":  TextInput(attrs={
                'class': "form-control",
                'label': "System's model",
                'placeholder': "Your system's model",                
            }),
            "location":  TextInput(attrs={
                'class': "form-control",
                'label': "System's location",
                'placeholder': "Your system's location",                
            }),
        }

