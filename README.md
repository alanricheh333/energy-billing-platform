
# Energy Billing System

This is a multi-service energy billing system built with Django and Celery, supporting user authentication, energy consumption tracking, billing, and invoice generation, including asynchronous task handling with Celery and RabbitMQ.

## Prerequisites

- Python 3.8+
- Django 4.x
- RabbitMQ
- Celery
- Redis (for Django session cache, optional but useful)
- PostgreSQL (optional, SQLite is used by default)
- WeasyPrint (for PDF generation)

## Table of Contents
- [Installation](#installation)
  - [Python Setup](#python-setup)
  - [Installing RabbitMQ](#installing-rabbitmq)
  - [Running RabbitMQ](#running-rabbitmq)
- [Setting Up Celery](#setting-up-celery)
- [Running the Django Application](#running-the-django-application)
- [Running Celery Workers](#running-celery-workers)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)

---

## Installation

### Python Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo-url.git
   cd energy-billing-system
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

---

## Installing RabbitMQ

RabbitMQ is required for Celery to handle background tasks.

### Installation on MacOS (using Homebrew)

1. **Install RabbitMQ**:
   ```bash
   brew install rabbitmq
   ```

2. **Start RabbitMQ**:
   ```bash
   brew services start rabbitmq
   ```

3. **Check RabbitMQ status**:
   ```bash
   brew services list
   ```

4. **Access RabbitMQ Management UI** (optional):
   - Enable RabbitMQ Management Plugin:
     ```bash
     rabbitmq-plugins enable rabbitmq_management
     ```
   - Access the RabbitMQ UI at `http://localhost:15672`.
   - Default credentials: `guest` / `guest`.

---

## Setting Up Celery

Celery is used to handle background tasks such as generating PDFs and sending email notifications.

### Celery Configuration

1. **Open your Django settings file** (`settings.py`) and ensure the following Celery settings are configured:
   
   ```python
   # settings.py

   CELERY_BROKER_URL = 'amqp://localhost'  # Default RabbitMQ URL
   CELERY_RESULT_BACKEND = 'rpc://'  # Default result backend for RabbitMQ
   CELERY_ACCEPT_CONTENT = ['json']
   CELERY_TASK_SERIALIZER = 'json'
   CELERY_RESULT_SERIALIZER = 'json'
   ```

2. **Set up Celery in Django project** (inside `energy_billing/celery.py`):
   ```python
   from celery import Celery
   import os

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'energy_billing.settings')
   app = Celery('energy_billing')
   app.config_from_object('django.conf:settings', namespace='CELERY')
   app.autodiscover_tasks()
   ```

---

## Running the Django Application

1. **Run the server**:
   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000`.

---

## Running Celery Workers

In order to process background tasks (e.g., generating invoices, sending email notifications), you need to start the Celery worker.

1. **Run the Celery worker**:
   ```bash
   celery -A energy_billing worker --loglevel=info
   ```

2. **Run the Celery beat scheduler** (for periodic tasks):
   ```bash
   celery -A energy_billing beat --loglevel=info
   ```

---

## Running Tests

The project contains test cases for different apps (authentication, consumption, billing, invoice). We also use **Robot Framework** for automated tests.

### Running Django Unit Tests:

1. **Run Django tests**:
   ```bash
   python manage.py test {test_file}
   ```

### Running Robot Framework Tests:

1. **Run Robot Framework tests**:
   ```bash
   robot apps/authentication/tests/robot_tests/
   ```

---

## API Documentation

Swagger has been integrated to provide API documentation.

1. **Access Swagger UI**:
   - Visit `http://127.0.0.1:8000/swagger/` to see the Swagger documentation.

2. **Redoc Documentation**:
   - Visit `http://127.0.0.1:8000/redoc/` for Redoc-based API documentation.

---

## Recurrent Task with Celery

We have implemented a recurring Celery task to send email reminders for overdue invoices every hour. This is handled by **Celery Beat**.

1. **Start Celery Beat for scheduling tasks**:
   ```bash
   celery -A energy_billing beat --loglevel=info
   ```

2. **Add Periodic Task** (already included in `settings.py`):
   ```python
   from celery.schedules import crontab

   CELERY_BEAT_SCHEDULE = {
       'send-overdue-invoice-reminder-every-hour': {
           'task': 'apps.invoices.tasks.send_overdue_invoice_reminder',
           'schedule': crontab(minute=0, hour='*'),  # Every hour
       },
   }
   ```

This task sends an email notification for unpaid invoices once an hour.

---

## Media and PDF Generation

We use **WeasyPrint** to generate invoice PDFs, which are stored in the `media/invoices/` directory.

### Ensure Media Folder Exists:

1. In your `settings.py`, make sure you have the following configured:
   ```python
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   MEDIA_URL = '/media/'
   ```

2. Create the `media/` folder if it doesn’t exist:
   ```bash
   mkdir media
   ```

---

## Conclusion

This project integrates user management, energy consumption tracking, billing, and invoicing using Django. Celery and RabbitMQ handle background tasks like generating PDFs and sending emails. Swagger is integrated for API documentation, and the project includes Robot Framework tests for validation.

Make sure you have all the necessary dependencies installed, and follow the steps outlined above to get the project running locally on your Mac.

If you have any issues or questions, feel free to reach out!
