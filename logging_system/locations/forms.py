from django import forms
from django.forms import TextInput

from .models import Location



class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = [
            "name",
            "town",
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
            "town": TextInput(attrs={
                'class': "form-control",
                'label': "Location's town and post code",
                'placeholder': "Your location's town and post code",
            }),
            "address": TextInput(attrs={
                'class': "form-control",
                'label': "Location's address",
                'placeholder': "Your location's address",
            }),
            "room": TextInput(attrs={
                'class': "form-control",
                'label': "Location's room",
                'placeholder': "Your location's room number",
            }),
            "notes": TextInput(attrs={
                'class': "form-control",
                'label': "Additional notes",
                'placeholder': "...",
            }),

        }
