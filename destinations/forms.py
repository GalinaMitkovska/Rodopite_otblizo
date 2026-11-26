
from django import forms
from django.core.exceptions import ValidationError

from .models import Destination


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = [
            'name',
            'category',
            'difficulty',
            'region',
            'description',
            'image',
        ]

        error_messages = {
            'name': {
                'unique': 'Забележителност с това име вече съществува!',
                'required': 'Моля, въведете име на забележителността.',
            }
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Име на забележителността',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-control',
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'напр. Триград, Смолян',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Опишете забележителността (поне 10 символа)...',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()

        if not name:
            raise ValidationError('Моля, въведете име.')

        return name

    def clean_region(self):
        region = self.cleaned_data['region'].strip()

        if not region:
            raise ValidationError('Моля, въведете район.')

        return region

    def clean_description(self):
        description = self.cleaned_data['description'].strip()

        if len(description) < 10:
            raise ValidationError(
                'Описанието трябва да съдържа поне 10 символа!'
            )

        return description


class DestinationUpdateForm(DestinationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].disabled = True
        self.fields['name'].help_text = (
            'Името на забележителността не може да се променя след създаване.'
        )


class DestinationSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Търсене',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Търси по име или регион...',
        }),
    )

    category = forms.ChoiceField(
        required=False,
        label='Категория',
        choices=[
            ('', 'Всички категории')
        ] + list(Destination.CATEGORY_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )
