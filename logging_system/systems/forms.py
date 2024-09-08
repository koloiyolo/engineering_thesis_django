from django import forms

from .models import System, Log

class SystemForm(forms.ModelForm):

    BOOL_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]
    SYSTEM_TYPE_CHOICES = [
    (0, 'Device'),
    (1, 'Service'),
    ]

    name            = forms.CharField(label="System name", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'System name'}))
    ip              = forms.CharField(label="IP address", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'System IP'}))
    system_type     = forms.ChoiceField(choices=SYSTEM_TYPE_CHOICES,widget=forms.RadioSelect,label="Is your system device or service?")
    to_ping         = forms.ChoiceField(choices=BOOL_CHOICES,widget=forms.RadioSelect,label="Do you wish to monitor latency of this system?") 
    email_notify    = forms.ChoiceField(choices=BOOL_CHOICES,widget=forms.RadioSelect,label="Do you wish to receive email notifications for abnormalities?") 
    port            = forms.CharField(label="Http port", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'System HTTP Port'}), required=False)
    model           = forms.CharField(label="System model", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'System model'}), required=False)
    location        = forms.CharField(label="Location", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'System location'}), required=False)

    class Meta:
        model = System
        fields = (
            "name",
            "ip",
            "system_type",
            "to_ping",
            "email_notify",
            "port",
            "model",
            "location")

