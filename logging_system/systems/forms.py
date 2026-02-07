from django import forms
from django.forms import NumberInput, Select, TextInput

from logging_system.locations.models import Location

from .models import SYSTEM_TYPE_CHOICES, System


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
            "location",
            "notes",
        ]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "label": "System's name",
                    "placeholder": "Your system's name",
                }
            ),
            "ip": TextInput(
                attrs={
                    "class": "form-control",
                    "label": "IP address",
                    "placeholder": "Your system's ip address",
                }
            ),
            "system_type": Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "to_ping": Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "email_notify": Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "port": NumberInput(attrs={"class": "form-control", "placeholder": ""}),
            "model": TextInput(
                attrs={
                    "class": "form-control",
                    "label": "System's model",
                    "placeholder": "Your system's model",
                }
            ),
            "location": Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "notes": TextInput(
                attrs={
                    "class": "form-control",
                    "label": "Additional notes",
                    "placeholder": "...",
                }
            ),
        }


class DiscoverSystemsForm(forms.Form):
    """Form to initiate the discover_systems_task."""

    ip_range = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "192.168.1.1-254",
                "label": "IP Address Range",
                "class": "form-control",
            }
        ),
    )
    system_type = forms.ChoiceField(
        choices=SYSTEM_TYPE_CHOICES,  # Dynamically get choices from the model
        required=True,
        widget=forms.Select(
            attrs={"label": "Type of found systems", "class": "form-control"}
        ),
    )
    prefix = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your optional prefix. Leave empty if none",
                "label": "Prefix",
                "class": "form-control",
            }
        ),
    )


class ReportSystemsForm(forms.Form):
    """Form to initiate the discover_systems_task."""

    ip_range = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "192.168.1.1-254",
                "label": "IP Address Range",
                "class": "form-control",
            }
        ),
    )
    system_type = forms.ChoiceField(
        choices=SYSTEM_TYPE_CHOICES,  # Dynamically get choices from the model
        required=True,
        widget=forms.Select(
            attrs={"label": "Type of found systems", "class": "form-control"}
        ),
    )
    prefix = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your optional prefix. Leave empty if none",
                "label": "Prefix",
                "class": "form-control",
            }
        ),
    )
