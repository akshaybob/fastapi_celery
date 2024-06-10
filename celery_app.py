"""Modules responsible for celery job run"""
from celery_config import celery
import tasks

if __name__ == "__main__":
    celery.start()
