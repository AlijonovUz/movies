from django.core.mail import send_mail
from celery import shared_task


@shared_task(bind=True)
def send_welcome_mail(self, subject, message, from_email, recipient_list):
    send_mail(
        subject,
        message,
        from_email,
        recipient_list
    )
