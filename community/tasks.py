from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_new_story_email(story_title, author_username, recipient_email):
    if not recipient_email:
        return False

    send_mail(
        subject=f'Nov pytepis: {story_title}',
        message=(
            f'Potrebitelqt {author_username} publikuva nov pytepis: "{story_title}".'
        ),
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@rodopite-otblizo.bg'),
        recipient_list=[recipient_email],
        fail_silently=True,
    )
    return True