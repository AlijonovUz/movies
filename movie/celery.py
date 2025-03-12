from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie.settings')

app = Celery('movie')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Tashkent')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Response: {self.request!r}')