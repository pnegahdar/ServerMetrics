from configs.redisdb import *
import time
import redis


class RedisMetrics(object):
    def __init__(self):
        self.gauges = []
        self.processed = False
        self.process()


    def add_gauge(self, name, value, source, measure_time=None, scale = False):
        if scale:
            value = value / float(SCALE)
        if not isinstance(measure_time, float):
            measure_time = time.time()
        data = {
            'name': name,
            'value': value,
            'source': source,
            'measure_time': int(measure_time),
            }
        self.gauges.append(data)


    def process(self):
        if self.processed:
            raise RuntimeError('Already processed once!')
        self.processed = True
        for each in REDIS_SERVERS:
            try:
                host = each.get('host', 'localhost')
                port = each.get('port', 6379)
                db = each.get('db', 0)
                password = each.get('password', None)
                source = 'Redis-{}:{}'.format(host, port)
                connection = redis.StrictRedis(host=host,
                    port=port, db=db, password=password)
                if IS_UP: self.add_gauge('is_up', 1, source)
                stats = connection.info()
                if USED_MEMORY: self.add_gauge('used_memory', stats['used_memory'], source, scale=True)
                if USED_CPU_SYS: self.add_gauge('used_cpu_sys', stats['used_cpu_sys'], source)
                if EVICTED_KEY_COUNT: self.add_gauge('evicted_keys', stats['evicted_keys'], source)
                if EXPIRED_KEY_COUNT: self.add_gauge('expired_keys', stats['expired_keys'], source)
                if USED_MEMORY_RSS: self.add_gauge('expired_keys', stats['expired_keys'], source, scale=True)
                if MEM_FRAGMENTATION_RATIO: self.add_gauge('used_memory_rss', stats['used_memory_rss'], source)
                key_total = 0
                for key, value in stats.items():
                    if key.startswith('db'):
                        key_total += value['keys']
                if KEY_COUNT: self.add_gauge('key_count', key_total, source)
            except redis.exceptions.ConnectionError:
                if IS_UP: self.add_gauge('is_on', 0, source)

    def get_gauges(self):
        return self.gauges


