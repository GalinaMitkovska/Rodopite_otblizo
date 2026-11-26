from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

UserModel = get_user_model()


def validate_min_length(value):
    cleaned_value = value.strip()

    if len(cleaned_value) < 10:
        raise ValidationError(
            'Описанието трябва да бъде поне 10 символа.'
        )



class Destination(models.Model):
    CATEGORY_CHOICES = [
        ('cave', 'Пещера'),
        ('waterfall', 'Водопад'),
        ('peak', 'Връх'),
        ('eco_trail', 'Екопътека'),
        ('fortress', 'Крепост / Исторически обект'),
        ('other', 'Друго'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Лесен'),
        ('moderate', 'Среден'),
        ('hard', 'Труден'),
    ]

    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name='Име на забележителността',
        error_messages={
            'unique': 'Вече съществува забележителност с това име.',
        }
    )
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='eco_trail',
        verbose_name='Категория',
    )
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='easy',
        verbose_name='Трудност на маршрута',
    )
    region = models.CharField(
        max_length=100,
        verbose_name='Район / Населено място',
    )
    description = models.TextField(
        validators=[validate_min_length],
        verbose_name='Описание',
    )
    image = models.ImageField(
        upload_to='destinations/',
        blank=True,
        null=True,
        verbose_name='Снимка',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата на добавяне',
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='destinations',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Забележителност'
        verbose_name_plural = 'Забележителности'

    def __str__(self):
        return self.name
