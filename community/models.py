from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class TravelStory(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name='Заглавие на пътеписа',
    )
    content = models.TextField(
        verbose_name='Разкажете вашата история или опит',
    )
    image = models.ImageField(
        upload_to='stories/',
        blank=True,
        null=True,
        verbose_name='Снимка от пътуването',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата на публикуване',
    )

    # Many-to-One връзка: Автор на пътеписа
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='stories',
        verbose_name='Автор',
    )

    destination = models.ForeignKey(
        'destinations.Destination',
        on_delete=models.CASCADE,
        related_name='stories',
        verbose_name='Свързана забележителност',
    )

    likes = models.ManyToManyField(
        UserModel,
        blank=True,
        related_name='liked_stories',
        verbose_name='Харесвания',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пътепис'
        verbose_name_plural = 'Пътеписи'

    def __str__(self):
        return f"{self.title} от {self.author.username}"
