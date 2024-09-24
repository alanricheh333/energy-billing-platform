import os
from celery import Celery # type: ignore

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'energy_billing.settings')

app = Celery('energy_billing')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery will auto-discover tasks from each Django app that has a tasks.py file
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
