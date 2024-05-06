from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import json
import numpy as np

from .models import Dataset, MlModel

from .dataset import create_dataset
from .functions import numpy_array_to_list
from .ml_models import create_model

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


class AddDatasetForm(forms.ModelForm):
    name     = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Dataset name', 'class': 'form-control'}))
    count    = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Data count', 'class': 'form-control'}))
    clusters = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Clusters count', 'class': 'form-control'}))
    data     = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Dataset
        fields = (
            'name', 
            'count',
            'clusters', 
            'data'
            )

    def save(self, commit=True):
        dataset = super().save(commit=False)

        
        count    = int(self.cleaned_data.get('count'))
        clusters = int(self.cleaned_data.get('clusters'))

        data = numpy_array_to_list(create_dataset(dataset_size=count, n_clusters=clusters))

        if data is not None:
            dataset.data = json.dumps(data)
        else:
            dataset.data = json.dumps({})

        if commit:
            dataset.save()
        return dataset


class AddModelForm(forms.ModelForm):
    name          = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Model name', 'class': 'form-control'}))
    model_type    = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices = {'knn': 'KNN', 'nn': 'Neural Network', 'rf': 'Random Forest', 'nb': 'Naive Bayes', 'svm': 'Support Vector Machines'})
    args          = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Arguments', 'class': 'form-control'}))
    dataset_id    = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Dataset ID', 'class': 'form-control'}))
    accuracy      = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = MlModel
        fields = (
            'name', 
            'model_type',
            'args', 
            'dataset_id',
            'accuracy',
            )

    def save(self, commit=True):
        model_object = super().save(commit=False)

        name          = str(self.cleaned_data.get('name'))
        dataset_id    = int(self.cleaned_data.get('dataset_id'))
        model_type    = str(self.cleaned_data.get('model_type'))
        args          = str(self.cleaned_data.get('args'))

        model, accuracy = create_model(name=name, dataset_id = dataset_id, model_type = model_type, args = args)
        
        
        if model is not None:
            model_object.accuracy = accuracy
            model_object.file = model 
        else:
            model_object.accuracy = '0'

        if commit:
            model_object.save()
        return model_object