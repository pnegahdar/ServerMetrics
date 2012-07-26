from collectors.mongodb import MongoDBMetrics
from collectors.redisdb import RedisMetrics
from settings import metric_server
import datetime
from pytz import utc
from settings import celery

@celery.task
def send_mongodb():
    to_send = {
        'gauges': MongoDBMetrics().get_gauges()
    }
    print "Mongodb Metrics update: {}".format(datetime.datetime.now(utc))
    metric_server.post_metrics(to_send)


@celery.task
def send_redisdb():
    to_send = {
        'gauges': RedisMetrics().get_gauges()
    }
    print "Redis Metrics update: {}".format(datetime.datetime.now(utc))
    metric_server.post_metrics(to_send)
