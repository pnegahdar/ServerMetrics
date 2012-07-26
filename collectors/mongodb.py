import pymongo
import time
from configs.mongodb import *
from pymongo.errors import ConnectionFailure

class MongoDBMetrics(object):

    def __init__(self):
        self.gauges = []
        self.processed = False
        self.process()


    def add_gauge(self, name, value, source, measure_time = None):
        if not measure_time: measure_time = time.time()
        data = {
            'name' : name,
            'value' : value,
            'source' : source,
            'measure_time' : int(measure_time),
        }
        self.gauges.append(data)


    def process(self):
        if self.processed:
            raise RuntimeError('Already processed once!')
        self.processed = True
        for each in MONGODB_SERVERS:
            source = 'MongoDB-{}:{}'.format(each['host'], each['port'])
            uri = 'mongodb://{}:{}@{}'.format(each['username'], each['password'],  each['host'])
            try:
                connection = pymongo.Connection(uri, port=each['port'])
                if IS_UP: self.add_gauge('is_on', 1, source)
                dbs = connection.database_names()
                index_sizes = 0
                storage_sizes = 0
                num_objects = 0
                num_collections = 0
                for database in dbs:
                    db_source = source + '-DB-{}'.format(database)
                    db = connection[database]
                    stats =  db.command('dbStats', scale=SCALE)
                    index_sizes += stats['indexSize']
                    storage_sizes += stats['storageSize']
                    num_objects += stats['objects']
                    num_collections += stats['collections']
                    if database in each['databases']:
                        if DB_NUM_INDEXES: self.add_gauge('index_count', stats['indexes'], db_source)
                        if DB_NUM_COLLECTIONS: self.add_gauge('collection_count', stats['collections'], db_source)
                        if DB_AVR_OBJ_SIZE: self.add_gauge('avrg_object_size', stats['avgObjSize'], db_source)
                        if DB_NUM_OBJECTS: self.add_gauge('object_count', stats['objects'], db_source)
                        if DB_STORAGE_SIZE: self.add_gauge('storage_size', stats['storageSize'], db_source)
                if TOTAL_INDEX_SIZE: self.add_gauge('total_index_size', index_sizes, source)
                if TOTAL_COLLECTIONS: self.add_gauge('total_collections', num_collections, source)
                if TOTAL_NUM_OBJECTS: self.add_gauge('total_objects', num_objects, source)
                if TOTAL_STORAGE_SIZE: self.add_gauge('total_storage_size', storage_sizes, source)
            except ConnectionFailure:
                if IS_UP: self.add_gauge('is_up', 0, source)

    def get_gauges(self):
        return self.gauges
