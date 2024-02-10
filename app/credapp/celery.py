import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credapp.settings')

celery = Celery('credapp')
celery.config_from_object('django.conf:settings', namespace='CELERY')

celery.autodiscover_tasks()
