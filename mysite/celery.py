from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Create the Celery app instance
app = Celery('mysite')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks from installed apps
app.autodiscover_tasks()

# Define the Celery Beat schedule for tasks
app.conf.beat_schedule = {
    'update-savings-accounts-every-minute': {
        'task': 'polls.tasks.update_savings_accounts',
        'schedule': crontab(minute='*'),  # Every minute
    },
    'update-loan-every-minute': {
        'task': 'polls.tasks.update_loan',
        'schedule': crontab(minute='*'),  # Every minute
    },
}

