import os
from datetime import timedelta
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object("django.conf:settings",namespace='CELERY')
app.autodiscover_tasks(packages=['auth_jatal'])

app.conf.beat_schedule = {
    'users-site': {
        'task': 'auth_jatal.tasks.users_site',
        'schedule': timedelta(seconds=10),
        'args': (),
    }
}
