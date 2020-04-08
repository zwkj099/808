# -*- coding: UTF-8 -*-
from redis_connect import RedisConnect
import json

def getredis(key,host,db,pwd):
    rdb = RedisConnect(host,db,pwd)
    key = key+'-location'
    value=rdb.get(key)
    if value!=None:
        result=json.loads(value)#将unicode转为字典
    else:
        return None
    return result

def get_0partition_keys(host,db,pwd):
    rdb = RedisConnect(host, 0, pwd)
    keys = rdb.getkeys()
    print keys
    id = []
    for key in keys:
        if key.find("-vehiclemsgsn") != -1:
            id.append((key.replace("-vehiclemsgsn", "")))

    print id
    return id




