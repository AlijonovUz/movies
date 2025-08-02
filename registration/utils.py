from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from .tasks import send_message


def send_verification_email(user, request):

    project_name = "MovieHub"
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verify_url = request.build_absolute_uri(
        reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
    )

    email = [user.email]
    subject = "Elektron pochtangizni tasdiqlang!"
    message = (
        f"Assalomu alaykum, {user.username}!\n\n"
        f"Siz bizning platformamizda ro'yxatdan o'tdingiz.\n"
        f"Ro'yxatdan o'tishni yakunlash va hisobingizni faollashtirish uchun quyidagi havolani bosing:\n\n"
        f"{verify_url}\n\n"
        f"Agar bu amalni siz bajarmagan bo‘lsangiz, iltimos, bu xabarni e'tiborsiz qoldiring.\n\n"
        f"— Hurmat bilan {project_name} jamoasi!"
    )

    send_message.delay(subject, message, email)

