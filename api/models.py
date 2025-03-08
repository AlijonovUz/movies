from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from registration.models import MyUser


class Genres(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Movies(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    description = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=8, default='00:00:00')
    language = models.CharField(max_length=15, default='O\'zbek tilida')
    year = models.PositiveIntegerField(default=1900,
                                       validators=[
                                           MinValueValidator(1900),
                                           MaxValueValidator(datetime.now().year)
                                       ])

    like = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    dislike = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    view = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    photo = models.ImageField(upload_to='movies/')
    genre = models.ManyToManyField(Genres, related_name='movies')

    def __str__(self):
        return self.title


class MovieReaction(models.Model):
    reaction = models.CharField(max_length=7)
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)