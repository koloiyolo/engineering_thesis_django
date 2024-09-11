from django import forms
from django.forms import TextInput, EmailInput, NumberInput, Select
import json
import numpy as np
from django.contrib.auth.models import User

from .models import Comment, Incident

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "message"
        ]

        widgets = {
            "message": TextInput(attrs={
                'class': "form-control",
                'label': "Comment",
                'placeholder': "Your comment..."
            })
        }