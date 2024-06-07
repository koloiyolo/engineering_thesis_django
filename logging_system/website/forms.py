from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import json
import numpy as np
from datetime import datetime

from .models import Log, Device, Service

from .functions import numpy_array_to_list

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email address'}))
    first_name = forms.CharField(label="", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name'}))
    last_name = forms.CharField(label="", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last name'}))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'



class DeviceForm(forms.ModelForm):

    EMAIL_NOTIFY_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    name            = forms.CharField(label="Device name", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device name'}))
    ip              = forms.CharField(label="IP address", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device IP'}))
    email_notify    = forms.ChoiceField(choices=EMAIL_NOTIFY_CHOICES,widget=forms.RadioSelect,label="Do you want to receive email notifications for abnormalities?") 
    port            = forms.CharField(label="Http port", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device HTTP Port'}), required=False)
    model           = forms.CharField(label="Device model", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device model'}), required=False)
    location        = forms.CharField(label="Location", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device location'}), required=False)

    class Meta:
        model = Device
        fields = (
            "name",
            "ip",
            "email_notify",
            "port",
            "model",
            "location")


class ServiceForm(forms.ModelForm):


    EMAIL_NOTIFY_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]


    name            = forms.CharField(label="Service name", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device name'}))
    ip              = forms.CharField(label="IP address", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device IP'}))
    email_notify    = forms.ChoiceField(choices=EMAIL_NOTIFY_CHOICES,widget=forms.RadioSelect,label="Do you want to receive email notifications for abnormalities?") 
    port            = forms.CharField(label="Http port", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device HTTP Port'}), required=False)
    service_type    = forms.CharField(label="Service type", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Service type'}))


    class Meta:
        model = Service
        fields = (
            "name",
            "ip",
            "email_notify",
            "port",
            "service_type")