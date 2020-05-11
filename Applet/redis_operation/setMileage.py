# -*- coding: utf-8 -*-

import datetime

import db_operation
from Applet.redis_operation import getdb_value

dbop = db_operation.db_operation()

def setto_redismel(key,ex808dict,host,db,pwd):
    """
    :param key:vehicle_id
    :param ex808dict:ex808dict字典参数
    :param host:redis ip
    :param db:redis 分区
    :param pwd:redis密码
    :return:exe808dict['me'] 里程值
    获取redis最后一条数据的里程值，并设置里程值，如果没有里程值，不设置，使用testconfig.xml中的默认里程值
    """

    # 判断当前时间是否是今天且是否有最后里程，如果有今天有最后里程，取redis的值，否则取testconfig里的mel值
    # 获取当前时间
    now = datetime.datetime.now()
    # 获取今天零点
    zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)

    redis_value = getdb_value.getredis(key, host, db, pwd)  #获取某个车辆id的redis中所有值



    try:
        redis_gpstime = redis_value['data']['msgBody']['gpsTime']#获取gpstime
        if datetime.datetime.strptime(redis_gpstime ,'%y%m%d%H%M%S' ) >zeroToday  :  # 如果gps时间是今天时间
            redis_mel = redis_value['data']['msgBody']['gpsMileage']#获取里程值
            if redis_mel!= None: #如果里程不为空，则设当前里程为redis里程
                ex808dict['mel'] = int(redis_mel)
            else:
                pass
    except:
        pass

    return ex808dict