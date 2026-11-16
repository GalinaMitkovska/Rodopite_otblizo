from django import forms
from .models import Producer


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = ['name', 'product_type', 'region', 'phone', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Име на стопанството'}),
            'product_type': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'напр. с. Широка лъка'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон за връзка'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишете вашите продукти...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }