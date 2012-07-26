MONGODB_SERVERS = [
        {
        'username': '',
        'password': '',
        'host': 'localhost',
        'port': 27017,
        'databases': ['', '', ''] #Databases to included for individual report, all are in the the aggregate reporting
    }
]

SCALE = 1024 * 1024 #1024 = KB, 1024*1024 = MB and so on

#Connection Level
IS_UP = True #Checks is up, 1 for is 0 for isnt.


#Database Level
DB_NUM_INDEXES = True
DB_NUM_OBJECTS = True
DB_NUM_COLLECTIONS = True
DB_AVR_OBJ_SIZE = True
DB_STORAGE_SIZE = True

#DATABASE AGGREGATES:
TOTAL_INDEX_SIZE = True
TOTAL_STORAGE_SIZE = True
TOTAL_NUM_OBJECTS = True
TOTAL_COLLECTIONS = True

