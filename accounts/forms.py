from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import AppUser, UserProfile


class AppUserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Local Partners', 'Локален партньор (Домакин или Производител)'),
        ('Content Moderators', 'Модератор на съдържание'),
        ('RegularUser', 'Обикновен потребител'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='Изберете роля в сайта:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = ('username', 'email')
        labels = {
            'username': 'Потребителско име',
            'email': 'Имейл адрес',
        }
        help_texts = {
            'username': 'Задължително. До 150 символа. Само букви, цифри и знаците @/./+/-/_',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Въведете потребителско име'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'vashia@email.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'password1' in self.fields:
            self.fields['password1'].label = 'Парола'
            self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Въведете парола'})
            self.fields['password1'].help_text = 'Паролата трябва да е поне 8 символа и да съдържа букви и цифри.'

        if 'password2' in self.fields:
            self.fields['password2'].label = 'Потвърждение на паролата'
            self.fields['password2'].widget.attrs.update(
                {'class': 'form-control', 'placeholder': 'Въведете паролата отново'})
            self.fields['password2'].help_text = 'Въведете същата парола за потвърждение.'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Създаване на потребителския профил
            UserProfile.objects.get_or_create(user=user)

            # Добавяне към съответната роля (група)
            role_name = self.cleaned_data.get('role')
            if role_name and role_name != 'RegularUser':
                group, _ = Group.objects.get_or_create(name=role_name)
                user.groups.add(group)

        return user