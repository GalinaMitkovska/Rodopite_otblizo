from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Accommodation(models.Model):
    TYPE_CHOICES = [
        ('guest_house', 'Къща за гости'),
        ('hotel', 'Семеен хотел'),
        ('hut', 'Планинска хижа'),
        ('eco_village', 'Еко селище'),
    ]

    name = models.CharField(
        max_length=120,
        verbose_name='Име на мястото за настаняване',
    )
    accommodation_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default='guest_house',
        verbose_name='Тип настаняване',
    )
    region = models.CharField(
        max_length=100,
        verbose_name='Населено място',
    )
    price_per_night = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Цена за нощувка',
    )
    capacity = models.PositiveIntegerField(
        verbose_name='Капацитет (брой места)',
    )
    description = models.TextField(
        verbose_name='Описание и удобства',
    )
    image = models.ImageField(
        upload_to='accommodations/',
        blank=True,
        null=True,
        verbose_name='Снимка',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата на добавяне',
    )

    owner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='accommodations',
        verbose_name='Собственик',
    )

    nearby_destinations = models.ManyToManyField(
        'destinations.Destination',
        blank=True,
        related_name='nearby_accommodations',
        verbose_name='Близки забележителности',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Място за настаняване'
        verbose_name_plural = 'Места за настаняване'

    def __str__(self):
        return f"{self.name} ({self.region}) - {self.price_per_night}."
