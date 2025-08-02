from django.core.mail import EmailMessage
from celery import shared_task
from django.conf import settings


@shared_task
def send_message(subject, message, bcc_list):
    if not bcc_list:
        return 'No recipient specified'

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=bcc_list
    )
    email.send()