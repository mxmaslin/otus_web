import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursera_webpack.settings')

os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

import configurations
configurations.setup()

app = Celery('coursera_webpack')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
