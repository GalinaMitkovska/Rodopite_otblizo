from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Producer(models.Model):
    PRODUCT_CHOICES = [
        ('honey', 'Домашен мед и пчелни продукти'),
        ('herbs', 'Билки и чай'),
        ('dairy', 'Млечни продукти (сирене, кашкавал)'),
        ('crafts', 'Занаяти и сувенири'),
        ('meat', 'Месни деликатеси'),
    ]

    name = models.CharField(
        max_length=120,
        verbose_name='Име на производител / стопанство',
    )
    product_type = models.CharField(
        max_length=30,
        choices=PRODUCT_CHOICES,
        default='honey',
        verbose_name='Основен продукт',
    )
    region = models.CharField(
        max_length=100,
        verbose_name='Населено място',
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон за връзка',
    )
    description = models.TextField(
        verbose_name='Описание на продуктите и историята',
    )
    image = models.ImageField(
        upload_to='producers/',
        blank=True,
        null=True,
        verbose_name='Снимка на стопанството',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата на добавяне',
    )

    owner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='producers',
        verbose_name='Собственик / Партньор',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Местен производител'
        verbose_name_plural = 'Местни производители'

    def __str__(self):
        return f"{self.name} ({self.region})"
