from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import json
import numpy as np
from datetime import datetime

from .models import Log, ClassifiedData, Device

from .dataset import create_dataset
from .functions import numpy_array_to_list
from .classification import classify

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


class ClassifyForm(forms.ModelForm):
    name          = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    model_type    = forms.ChoiceField(required=True, 
                                      widget=forms.RadioSelect, choices = {
                                                                            'kmeans': 'K-Means: General-purpose, even cluster size,flat geometry, not too many clusters, ', 
                                                                            'bkmean': 'Bisecting K-Means: General-purpose, even cluster size, flat geometry, no empty clusters, inductive, hierarchical', 
                                                                            'ms': 'Mean-Shift: Many clusters, uneven cluster size, non-flat geometry', 
                                                                            'ahc': 'Agglomerative hierarchical clustering: Many clusters, possibly connectivity constraints, ', 
                                                                            'ward': 'Ward hierarchical clustering: Many clusters, possibly connectivity constraints, transductive'})
    size          = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': 'Sample size', 'class': 'form-control'}))
    offset        = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': 'Sample offset', 'class': 'form-control'}))
    date          = forms.CharField(widget=forms.HiddenInput(), required=False)
    data          = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ClassifiedData
        fields = (
            'name', 
            'model_type',
            'size',
            'offset',
            'date',
            'data' 
            )
    
    def save(self, commit=True):
        cdata = super().save(commit=False)

        
        size    = int(self.cleaned_data.get('size'))
        offset  = int(self.cleaned_data.get('offset'))
        model_type = str(self.cleaned_data.get('model_type'))

        cdata.date = datetime.now()

        data = numpy_array_to_list(classify(model_type=model_type, size=size, offset=offset))

        if data is not None:
            cdata.data = json.dumps(data)
        else:
            cdata.data = json.dumps({})

        if commit:
            cdata.save()
        return cdata

# class AddKmeansForm(forms.ModelForm):
#     name           = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Model name', 'class': 'form-control'}))
#     model_type     = forms.CharField(widget=forms.HiddenInput(), required=False)
#     args           = forms.CharField(widget=forms.HiddenInput(), required=False)
#     n_clusters     = forms.IntegerField(label = 'Cluster count', widget=forms.widgets.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1}))

#     class Meta:
#         model = MlModel
#         fields = (
#             'name', 
#             'model_type',
#             'args', 
#             )

#     def save(self, commit=True):
#         mlmodel = super().save(commit=False)
#         n_clusters = int(self.cleaned_data.get('n_clusters'))
#         mlmodel.model_type = 'kmeans'
#         if n_clusters != 0:
#             mlmodel.args = json.dumps({'n_clusters': n_clusters})
#         else:
#             mlmodel.args = json.dumps({})
#         if commit:
#             mlmodel.save()
#         return mlmodel

# class AddBKmeansForm(forms.ModelForm):
#     name           = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Model name', 'class': 'form-control'}))
#     model_type     = forms.CharField(widget=forms.HiddenInput(), required=False)
#     args           = forms.CharField(widget=forms.HiddenInput(), required=False)
#     n_clusters     = forms.IntegerField(label = 'Cluster count', widget=forms.widgets.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1, }))

#     class Meta:
#         model = MlModel
#         fields = (
#             'name', 
#             'model_type',
#             'args', 
#             )

#     def save(self, commit=True):
#         mlmodel = super().save(commit=False)
#         n_clusters = int(self.cleaned_data.get('n_clusters'))
#         mlmodel.model_type = 'bkmeans'
#         if n_clusters != 0:
#             mlmodel.args = json.dumps({'n_clusters': n_clusters})
#         else:
#             mlmodel.args = json.dumps({})
#         if commit:
#             mlmodel.save()
#         return mlmodel

class DeviceForm(forms.ModelForm):

    name        = forms.CharField(label="Device name", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device name'}))
    ip          = forms.CharField(label="IP address", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device IP'}))
    model       = forms.CharField(label="Device model", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device model'}))
    location    = forms.CharField(label="Location", max_length="32", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Device location'}))

    class Meta:
        model = Device
        fields = (
            "name",
            "ip",
            "model",
            "location")
