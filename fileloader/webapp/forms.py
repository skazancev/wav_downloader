from django import forms
from .models import WAVFile


class WAVForm(forms.ModelForm):
    class Meta:
        model = WAVFile
        fields = ['file', 'number']
        widgets = {
            'number': forms.NumberInput()
        }


class WAVChangeForm(forms.ModelForm):
    class Meta:
        model = WAVFile
        fields = ['file', 'number', 'active']
