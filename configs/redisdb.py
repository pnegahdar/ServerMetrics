REDIS_SERVERS = [
        {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None,
    }
]
SCALE = 1024 * 1024 #1024 = KB, 1024*1024 = MB and so on

#Connection Level
IS_UP = True
USED_MEMORY = True
USED_CPU_SYS = True
KEY_COUNT = True
EVICTED_KEY_COUNT = True
MEM_FRAGMENTATION_RATIO = True
EXPIRED_KEY_COUNT = True
USED_MEMORY_RSS = True
