from django import forms
from django.forms import TextInput

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]

        widgets = {
            "message": TextInput(
                attrs={
                    "class": "form-control",
                    "label": "Comment",
                    "placeholder": "Your comment...",
                }
            )
        }
