# -*- coding: UTF-8 -*-
import redis

from db_operation.redis_connect import RedisConnect
import json

def getredis(key,host,db,pwd):
    """
    :param key: 车辆id
    :param host: redis ip
    :param db: redis 分区
    :param pwd: redis密码
    :return: 返回此车辆id的全部值
    """

    rdb = RedisConnect(host,db,pwd)
    key = key
    value=rdb.get(key)
    if value!=None:
        result=json.loads(value)#将unicode转为字典
    else:
        return None
    return result

def get_0partition_keys(host,db,pwd):
    """
    :param host: redis ip
    :param db: redis 分区
    :param pwd: redis 密码
    :return: 返回以"-vehiclemsgsn"为结尾的所有key值
    """
    rdb = RedisConnect(host, 0, pwd)
    keys = rdb.getkeys()
    print keys
    id = []
    for key in keys:
        if key.find("-vehiclemsgsn") != -1:
            id.append((key.replace("-vehiclemsgsn", "")))

    print id
    return id

def get_15partition_keys(host,db,pwd,key):

    pool = redis.ConnectionPool(host=host, port=6379, db=db,password=pwd,decode_responses=True)
    rdb = redis.StrictRedis(connection_pool=pool)
    keys = rdb.keys()
    value = rdb.get(key)

    print value
    # id = []
    # for key in keys:
    #     if key.find("-vehiclemsgsn") != -1:
    #         id.append((key.replace("-vehiclemsgsn", "")))
    #
    # print id
    return value



