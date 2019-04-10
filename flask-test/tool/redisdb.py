# -*- coding: utf-8 -*-
import time
import redis

class RedisQueue():
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.Redis(**redis_kwargs, host='47.106.37.156', password='Xc199704')
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)

class RedisSet():

    def __init__(self, key):
        self.__db = redis.StrictRedis()
        self.key = key

    def add(self, val, ttl=59):
        """Put an element which include ttl in zset.

        :param val: An element in zset.
        :param ttl: Time to live.
        :return: None
        """
        now = time.time()
        # Put the expiration time as ``score`` in the zset.
        self.__db.zadd(self.key, now+ttl, val)
        # Delete expired elements.
        self.__db.zremrangebyscore(self.key, '-inf', time.time())

    def rem(self, val):
        """Remove  ``val`` element

        :param val: element's name
        :return: None
        """
        self.__db.zrem(self.key, val)


    def getAll(self):
        """Get elements which still alive.

        :return: Alive elements.
        """
        self.__db.zremrangebyscore(self.key, '-inf', time.time())
        return self.__db.zrangebyscore(self.key, time.time(), '+inf')

    def get(self):
        """Get one element.

        :return: None or An element
        """
        sets = self.getAll()
        if sets:
            return sets[0]
        else:
            return None