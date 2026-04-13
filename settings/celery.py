# Celery Modules
from celery import Celery
import os
from celery.schedules import crontab

# Projects Modules
from settings.conf import ENV_ID


os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.env.{ENV_ID}')

app = Celery('blog')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_url = os.environ.get('BLOG_CELERY_BROKER_URL', 'redis://localhost:6379/1')
app.conf.result_backend = os.environ.get('BLOG_CELERY_BROKER_URL', 'redis://localhost:6379/1')

app.conf.beat_schedule = {
    'publish-scheduled-posts': {
        'taks': 'apps.blog.tasks.publish-scheduled-posts',
        'schedule': 60.0,
    },
    'clear-expired-notifications': {
        'taks': 'apps.notifications.tasks.clear-expired-notifications',
        'schedule': crontab(hour=3, minute=0),
    },
    'generate-daily-stats': {
        'taks': 'apps.blog.tasks.generate-daily-stats',
        'schedule': crontab(hour=0, minute=0),
    },
}





