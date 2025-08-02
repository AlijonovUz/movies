import re
from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Nomi")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Identifikatori")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Janr '
        verbose_name_plural = 'Janrlar'


class Country(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Nomi")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Identifikatori")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Mamlakat '
        verbose_name_plural = 'Mamlakatlar'


AGE_LIMITS = [
    ('0+', '0+'),
    ('6+', '6+'),
    ('12+', '12+'),
    ('16+', '16+'),
    ('18+', '18+')
]

LANGUAGE_CHOICES = [
    ('O\'zbek tilida', "O'zbek tilida"),
    ('Rus tilida', "Rus tilida"),
    ('Ingliz tilida', "Ingliz tilida")
]


class Movie(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name="Sarlavhasi")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Identifikatori")

    description = models.TextField(null=True, blank=True, verbose_name="Tavsifi")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='movies', verbose_name='Mamlakati')
    duration = models.CharField(max_length=30, default="1 soat 59 daqiqa 59 soniya", verbose_name="Davomiyligi")
    language = models.CharField(max_length=15, choices=LANGUAGE_CHOICES, verbose_name="Tili")
    year = models.PositiveIntegerField(default=datetime.now().year,
                                       validators=[
                                           MinValueValidator(1900),
                                           MaxValueValidator(datetime.now().year)
                                       ],
                                       verbose_name="Yili")

    age_limit = models.CharField(max_length=3, choices=AGE_LIMITS, verbose_name="Yosh chegarasi")

    like = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Yoqtirishlar")
    dislike = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Yoqtirmasliklar")
    view = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Ko'rishlar")

    photo = models.ImageField(upload_to='movies/', verbose_name="Surati")
    genre = models.ManyToManyField(Genre, related_name='movies', verbose_name="Janri")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Film '
        verbose_name_plural = 'Filmlar'
        ordering = ['-created_at']


TYPES_CHOICE = [
    ('trailer', "Treyler"),
    ('movie', "Film"),
    ('series', "Serial")
]


class MovieURL(models.Model):
    title = models.CharField(max_length=150, verbose_name="Sarlavhasi")
    type = models.CharField(max_length=10, choices=TYPES_CHOICE, verbose_name="Turi")
    part = models.PositiveIntegerField(null=True, blank=True, verbose_name="Qismi")

    embed_input = models.TextField(
        "Saytdan joylashtiriladigan video URL",
        help_text=(
            "YouTube yoki Mover.uz'dan quyidagi formatlarda <b>iframe</b> yoki <b>video URL</b> kiriting:<br><br>"
            "<b>Masalan (Film yoki Serial uchun):</b><br>"
            "<code>&lt;iframe src=\"https://www.youtube.com/embed/abc123\"&gt;&lt;/iframe&gt;</code><br>"
            "yoki<br>"
            "<code>https://mover.uz/video/embed/kb0pUqVX</code><br><br>"
            "<b>Agar turi <i>Treyler</i> bo‘lsa:</b><br>"
            "Oddiy video URL havolasini kiriting, masalan:<br>"
            "<code>https://youtu.be/1ovgxN2VWNc</code>"
        )
    )

    embed_url = models.URLField("Tozalangan URL", editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_url', verbose_name="FIlmi")

    def clean(self):
        value = self.embed_input.strip()

        if self.type == "series":
            if self.part is None:
                raise ValidationError({
                    'part': "Serial uchun 'qism' majburiy."
                })
        else:
            if self.part is not None:
                raise ValidationError({
                    "part": "Faqat seriallar uchun 'qism' kiritiladi. Film yoki treyler uchun bo‘sh qoldiring."
                })

        if self.type != "trailer":
            match = re.search(r'src=["\'](.*?)["\']', value)
            if match:
                value = match.group(1)

            if not value.startswith('https://'):
                raise ValidationError({
                    "embed_input": "URL manzili noto'g'ri kiritildi."
                })
        else:
            if not value.startswith('https://'):
                raise ValidationError({
                    "embed_input": "Treyler uchun to'g'ri URL kiriting, masalan: https://youtu.be/xyz"
                })

        self.embed_url = value

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Havola '
        verbose_name_plural = 'Havolalar'
        ordering = ['movie', 'part']

        constraints = [
            models.UniqueConstraint(fields=['movie', 'part'], name='unique_movie_part')
        ]


class MovieReaction(models.Model):
    reaction = models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)