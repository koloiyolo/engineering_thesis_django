from django import forms

from .models import Device, Log

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

