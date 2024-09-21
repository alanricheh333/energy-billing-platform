from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'energy_billing.settings')

app = Celery('energy_billing')

# Load settings from Django settings, using the CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks from all registered apps
app.autodiscover_tasks()
