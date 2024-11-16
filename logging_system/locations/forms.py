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
                'label': "Location's name",
                'placeholder': "Your location's name",                
            }),
            "address": TextInput(attrs={
                'class': "form-control",
                'label': "Location's address",
                'placeholder': "Your location's address",                
            }),
            "room": TextInput(attrs={
                'class': "form-control",
                'label': "Location's room",
                'placeholder': "Your location's notes",                
            }),
            "notes": TextInput(attrs={
                'class': "form-control",
                'label': "Additional notes",
                'placeholder': "...",                
            }),

        }
