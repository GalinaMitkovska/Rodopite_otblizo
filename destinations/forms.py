from django import forms
from .models import Destination


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'category', 'difficulty', 'region', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Име на забележителността'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'напр. Триград, Смолян'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишете забележителността (поне 10 символа)...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'name': {
                'unique': 'Забележителност с това име вече съществува в системата!',
                'required': 'Моля, въведете име.',
            }
        }