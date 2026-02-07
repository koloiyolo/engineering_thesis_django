from django import forms

BOOL_CHOICES = [
    (True, "Yes"),
    (False, "No"),
]


class ExportToCsvForm(forms.Form):
    """Form to initiate the discover_systems_task."""

    file_name = forms.CharField(
        initial="logs",
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "eg. logs",
                "label": "Prefix",
                "class": "form-control",
            }
        ),
    )

    count = forms.IntegerField(
        initial=2000,
        required=False,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Leave empty for all",
                "label": "Log records count",
                "class": "form-control",
            }
        ),
    )

    with_labels = forms.BooleanField(  # Dynamically get choices from the model
        required=False,
        widget=forms.Select(
            choices=BOOL_CHOICES,
            attrs={"label": "Type of found systems", "class": "form-control"},
        ),
    )
