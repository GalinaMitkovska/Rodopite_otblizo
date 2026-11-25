from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AppUser, UserProfile


@receiver(post_save, sender=AppUser)
def handle_new_user_registration(sender, instance, created, **kwargs):
    if not created:
        return

    UserProfile.objects.get_or_create(user=instance)

    if not instance.is_superuser:
        registered_group, _ = Group.objects.get_or_create(name='Registered Users')
        instance.groups.add(registered_group)