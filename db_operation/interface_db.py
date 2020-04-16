# -*- coding: utf-8 -*-

'''
Created on 2019-8-18

@author: Administrator
'''
import MySQLdb

class interface_db(object):
    # def __init__(self,host_db='192.168.24.105',user_db='root',passwd_db='Zwkj@123Mysql',name_db='mysql',port_db=3306,link_type=0):
    #     '''
    #     :param host_db: 数据库服务主机
    #     :param user_db: 数据库用户名
    #     :param passwd_db: 数据库密码
    #     :param name_db: 数据库名称
    #     :param port_db: 端口号，整型数字
    #     :param link_type: 链接类型，用于输出数据是元祖还是字典，默认是字典，link_type=0
    #     :return:游标
    #     '''
    #     try:
    #         self.conn=MySQLdb.connect(host=host_db,user=user_db, passwd=passwd_db, db=name_db, port=port_db, charset='utf8')#创建数据库链接
    #         if link_type==0:
    #             self.cur=self.conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)#返回字典
    #         else:
    #             self.cur=self.conn.cursor()#返回元祖
    #     except MySQLdb.Error as e:
    #         print (u"创建数据库连接失败|Mysql Error %d: %s" % (e.args[0], e.args[1]))
    #
    def mysqldata(self,sql):    #连接数据库方法
        con=MySQLdb.connect(host ='192.168.24.105',user = 'root',passwd ='Zwkj@123Mysql',db = 'customer-center',port = 3306, charset = 'utf8')     #获取连接
        cur=con.cursor()    #获取游标
        cur.execute(sql)    #执行sql语句
        data=cur.fetchall()     #从游标中得到执行结果
        con.commit()    #提交事务
        con.close()     #关闭连接
        return data

                # self.cur.execute(sql)#执行sql语句
                # self.conn.commit()
    #     #数据库关闭
    #     def __del__(self):
    #         if self.cur != None:
    #             self.cur.close()
    #         if self.conn != None:
    #             self.conn.close()