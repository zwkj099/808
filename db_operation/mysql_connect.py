# -*- coding: UTF-8 -*-

import MySQLdb

class Mysql(object):
    def __init__(self,host,port,user,passwd,db,charset='utf8'):
        """初始化mysql连接"""
        try:
            self.conn = MySQLdb.connect(host,user,passwd,db,int(port),charset='utf8')
        except MySQLdb.Error as e:
            errormsg = 'Cannot connect to server\nERROR(%s):%s' % (e.args[0],e.args[1])
            print(errormsg)
            exit(2)
        self.cursor = self.conn.cursor()

    def exect(self,sql):
        """执行dml,ddl语句"""
        try:
           self.cursor.execute(sql)
           self.conn.commit()
        except:
           self.conn.rollback()

    def query(self,sql):
        """查询数据"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close_mysql(self):
        """ 关闭mysql连接 """
        self.conn.close()
        self.cursor.close()

