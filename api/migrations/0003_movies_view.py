# Generated by Django 5.1.3 on 2025-03-04 09:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_movies_slug_alter_movies_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='view',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
