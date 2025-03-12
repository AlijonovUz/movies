from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from registration.models import MyUser

from api.models import Movies
from api.tasks import send_mail_task


@receiver(post_save, sender=Movies)
def send_mail_on_new_movie(sender, instance, created, **kwargs):
    if created:
        subject = "Yangi film qo'shildi!"
        message = f"Bizda premyera!\n\n🎬 Film nomi: {instance.title}\n⏳ Davomiyligi: {instance.duration}\n🗣 Tili: {instance.language}"
        from_email = settings.DEFAULT_FROM_EMAIL

        recipient_list = list(MyUser.objects.filter(email__isnull=False).exclude(email="").values_list('email', flat=True))

        if recipient_list:
            send_mail_task.delay(subject, message, from_email, recipient_list)

