import os

from celery import Celery


cel = Celery('test', broker=os.environ.get('CELERY_BROKER'), backend=os.environ.get('CELERY_BACKEND'))


@cel.task
def run(x, y):
    return x * y


# celery -A test worker --loglevel=INFO --pool=solo
