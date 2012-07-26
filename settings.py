from __future__ import absolute_import
import os
from celery.schedules import crontab
import librato
from celery import Celery


API_USER_NAME = ''
API_KEY = ''
metric_server = librato.connect(API_USER_NAME, API_KEY)


BROKER_URL = os.getenv('REDISTOGO_URL', 'redis://localhost')
CELERY_RESULT_BACKEND = os.getenv('REDISTOGO_URL', 'redis://localhost')


celery = Celery(broker=BROKER_URL, backend=CELERY_RESULT_BACKEND, include=['tasks'])

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERYBEAT_SCHEDULE={
        'mongodb_metrics': {
            'task': 'tasks.send_mongodb',
            'schedule': crontab(),
            },

        'redisdb_metrics': {
            'task': 'tasks.send_redisdb',
            'schedule': crontab(),
            },
        }
)




