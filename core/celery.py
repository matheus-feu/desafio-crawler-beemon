from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

from app.helpers.setup_logger import logger

# Settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Celery
app = Celery('app', broker=os.environ.get('CELERY_BROKER_URL'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    result_expires=3600,
    enable_utc=True,
    task_concurrency=5,
    timezone='America/Sao_Paulo'
)
# Celery Beat Schedule
app.conf.beat_schedule = {
    'scrapy_task': {
        'task': 'scrapy_task',
        'schedule': crontab(hour='*', minute='*/20', day_of_week='*'),
        'args': ('https://www.imdb.com/chart/top/', 'csv'),
    }
}
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    logger.info('Request: {0!r}'.format(self.request))
