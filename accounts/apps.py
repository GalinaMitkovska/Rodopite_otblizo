from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_user_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from accommodations.models import Accommodation
    from producers.models import Producer
    from destinations.models import Destination
    from community.models import TravelStory

    partners_group, _ = Group.objects.get_or_create(name='Local Partners')
    partner_models = [Accommodation, Producer]
    partner_permissions = []
    for model in partner_models:
        ct = ContentType.objects.get_for_model(model)
        perms = Permission.objects.filter(
            content_type=ct,
            codename__in=[f'add_{model._meta.model_name}', f'change_{model._meta.model_name}', f'view_{model._meta.model_name}']
        )
        partner_permissions.extend(perms)
    partners_group.permissions.set(partner_permissions)


    moderators_group, _ = Group.objects.get_or_create(name='Content Moderators')
    moderator_models = [Destination, TravelStory]
    moderator_permissions = []
    for model in moderator_models:
        ct = ContentType.objects.get_for_model(model)
        perms = Permission.objects.filter(
            content_type=ct,
            codename__in=[f'add_{model._meta.model_name}', f'change_{model._meta.model_name}', f'delete_{model._meta.model_name}', f'view_{model._meta.model_name}']
        )
        moderator_permissions.extend(perms)
    moderators_group.permissions.set(moderator_permissions)


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals
        post_migrate.connect(create_user_groups, sender=self)