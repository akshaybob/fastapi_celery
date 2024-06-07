from celery import Celery
import os

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery.conf.update(
    task_routes={
        'scheduler': {'queue': 'scheduler'},
        'executor': {'queue': 'executor'},
    },
    beat_schedule={
        'run-scheduler-daily': {
            'task': 'scheduler',
            'schedule': 100.0,  # Run daily 86400.0
        },
        'run-executor-every-5-mins': {
            'task': 'executor',
            'schedule': 300.0,  # Run every 5 minutes
        },
    }
)
