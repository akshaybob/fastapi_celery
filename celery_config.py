"""Module delas with Celery configuration """
from celery import Celery
import os
from dotenv import load_dotenv
from celery.schedules import crontab
from datetime import timedelta

load_dotenv()

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery.conf.update(
    beat_schedule={
        'run-scheduler-daily': {
            'task': 'scheduler',
            'schedule': crontab(hour=0, minute=0),
        },
        'run-executor-every-5-mins': {
            'task': 'executor',
            'schedule': timedelta(minutes=5),
        },
    },
    timezone='UTC'
)
