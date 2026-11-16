from django import forms
from .models import Accommodation


class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['name', 'accommodation_type', 'region', 'price_per_night', 'capacity', 'description', 'image', 'nearby_destinations']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'accommodation_type': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nearby_destinations': forms.CheckboxSelectMultiple(),
        }