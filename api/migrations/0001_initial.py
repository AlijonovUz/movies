# Generated by Django 5.1.3 on 2025-03-04 09:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('duration', models.CharField(default='00:00:00', max_length=8)),
                ('year', models.PositiveIntegerField(default=1900, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2025)])),
                ('like', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('dislike', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('photo', models.ImageField(upload_to='movies/')),
                ('genre', models.ManyToManyField(related_name='movies', to='api.genres')),
            ],
        ),
    ]
