from django import forms
from django.forms import TextInput

from .models import Location



class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = [
            "name",
            "address",
            "room",
            "notes"
        ]

        widgets = {
            "name": TextInput(attrs={
                'class': "form-control",
                'label': "System's name",
                'placeholder': "Your system's name",                
            }),
            "address": TextInput(attrs={
                'class': "form-control",
                'label': "System's name",
                'placeholder': "Your system's name",                
            }),
            "room": TextInput(attrs={
                'class': "form-control",
                'label': "System's name",
                'placeholder': "Your system's name",                
            }),
            "notes": TextInput(attrs={
                'class': "form-control",
                'label': "System's name",
                'placeholder': "Your system's name",                
            }),

        }
