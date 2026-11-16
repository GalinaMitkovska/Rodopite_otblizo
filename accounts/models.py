from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'Вече съществува потребител с този имейл адрес.',
        }
    )

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Име',
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Фамилия',
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='За мен',
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        verbose_name='Профилна снимка',
    )
    favorite_region = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Любим дял от Родопите',
    )
    favorite_destinations = models.ManyToManyField(
        'destinations.Destination',
        blank=True,
        related_name='favorited_by',
        verbose_name='Любими забележителности',
    )

    def __str__(self):
        return f"Профил на {self.user.username}"
