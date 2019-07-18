from django import forms
from .models import document


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    filename = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'style': 'display: none;'
            }
        )
    )

    class Meta:
        model = document
        fields = ('document')