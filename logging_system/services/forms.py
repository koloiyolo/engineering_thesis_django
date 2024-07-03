from django import forms

from .models import Service, Log

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
