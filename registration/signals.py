from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Message
from .tasks import send_message


@receiver(post_save, sender=Message)
def message_signal(sender, instance, created, **kwargs):
    if created:
        recipient_list = list(User.objects.filter(email__isnull=False).values_list('email', flat=True))
        subject = instance.subject
        message = instance.message
        send_message.delay(subject, message, recipient_list)