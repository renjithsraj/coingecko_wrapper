import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coingecko_wrapper.settings")
app = Celery("coingecko_wrapper")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


from celery.schedules import crontab


app.conf.beat_schedule = {
    'fetch-latest-btc-info': {
        'task': 'home.tasks.fetch_btc',
        'schedule': 30.0
    },
}