from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name="Mavzusi")
    message = models.TextField(verbose_name="Xabar matni")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")

    def __str__(self):
        return f"{self.subject} - {self.created_at}"

    class Meta:
        verbose_name = "Xabar "
        verbose_name_plural = "Xabarlar"
        ordering = ['-created_at']


class BlacklistedAccessToken(models.Model):
    token = models.CharField(max_length=500)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
