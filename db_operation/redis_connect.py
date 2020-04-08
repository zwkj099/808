# -*- coding: UTF-8 -*-
from redis import ConnectionPool, Redis

class RedisConnect(object):
    def __init__(self, host, db, pwd):
        self.pool = ConnectionPool(host=host, port=6379, db=db, password=pwd,
                              decode_responses=True)
        self.rdb = Redis(connection_pool=self.pool)

    def set(self, key, value):
        return self.rdb.set(key, value)

    def get(self, key):
        if self.rdb.exists(key):
            return self.rdb.get(key)
        else:
            return None

    def getkeys(self):
        return self.rdb.keys()


