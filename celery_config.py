import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery.conf.update(
    beat_schedule={
        'run-scheduler-daily': {
            'task': 'scheduler',
            'schedule': 100.0,  # Run daily 86400.0
        },
        'run-executor-every-5-mins': {
            'task': 'executor',
            'schedule': 300.0,  # Run every 5 minutes
        },
    },
    timezone='UTC'
)
