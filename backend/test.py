from celery import Celery


app = Celery('tasks', backend='rpc://', broker='pyamqp://')


@app.task
def add(x, y):
    return x + y


# celery -A test worker --loglevel=INFO --pool=solo
