from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from registration.models import MyUser
from .tasks import send_welcome_mail


@receiver(post_save, sender=MyUser)
def send_mail_movie(sender, created, instance, **kwargs):
    if created:
        subject = "Ro'yxatdan o'tganingiz uchun rahmat!"
        message = (
            "Assalomu alaykum, hurmatli foydalanuvchi!\n\n"
            "Sizni bizning platformamizga qo‘shilganingiz bilan tabriklaymiz! 🎉\n"
            "Umid qilamizki, saytimiz siz uchun foydali va qulay bo‘ladi.\n\n"
            "Agar biron savollaringiz bo‘lsa yoki qo‘llab-quvvatlash kerak bo‘lsa, "
            "biz bilan bog‘lanishingiz mumkin.\n"
            "Sizga ajoyib tajriba va muvaffaqiyat tilaymiz!\n\n"
            "Hurmat bilan,\n"
            "MovieHub jamoasi"
        )

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        send_welcome_mail.delay(subject, message, from_email, recipient_list)
