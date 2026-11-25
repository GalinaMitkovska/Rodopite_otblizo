from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AppUser, UserProfile


class AppUserRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = ('username', 'email')

        labels = {
            'username': 'Потребителско име',
            'email': 'Имейл адрес',
        }

        help_texts = {
            'username': 'Задължително. До 150 символа.',
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Въведете потребителско име'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'vashia@email.com'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = 'Парола'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Въведете парола'
        })

        self.fields['password2'].label = 'Потвърждение на паролата'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Въведете паролата отново'
        })


class UserProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label='Потребителско име',
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
        labels = {
            'bio': 'Кратка информация за вас',
            'profile_picture': 'Профилна снимка',
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Разкажете накратко за себе си и любимите си места в Родопите...',
            }),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields['username'].initial = self.instance.user.username
