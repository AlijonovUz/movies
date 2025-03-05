from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=User)
def sendMail(sender, created, instance, **kwargs):
    if created:
        subject = "Ro'yxatdan o'tganingiz uchun rahmat!"
        from_email = settings.DEFAULT_FROM_EMAIL

        recipient_list = [instance.email]

        html_content = render_to_string('emails/index.html',{
            'username': instance.username,
            'current_year': datetime.now().year
        })

        email = EmailMultiAlternatives(
            subject=subject,
            from_email=from_email,
            to=recipient_list
        )

        email.attach_alternative(html_content, 'text/html')
        email.send(fail_silently=True)