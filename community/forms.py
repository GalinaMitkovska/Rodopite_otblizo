from django import forms
from .models import TravelStory


class TravelStoryForm(forms.ModelForm):
    class Meta:
        model = TravelStory
        fields = ['title', 'destination', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заглавие на пътеписа'}),
            'destination': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Споделете вашата история...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }