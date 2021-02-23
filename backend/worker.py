import os

import redis
from rq import Worker, Queue, Connection

queueToListen = ['tasksQueue']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, queueToListen)))
        worker.work()
