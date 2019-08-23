#__author__ = 'hrwang'
# -*- coding:utf-8 -*-
'''
定义对mysql数据库基本操作的封装
1.包括基本的单条语句操作，删除、修改、更新
2.独立的查询单条、查询多条数据
3.独立的添加多条数据
'''
import MySQLdb,logging,os
class operationdb_interface(object):
    def __init__(self,host_db='192.168.24.142',user_db='root',passwd_db='Zwkj@123Mysql',name_db='clbs',port_db=3306,link_type=0):
        '''
        :param host_db: 数据库服务主机
        :param user_db: 数据库用户名
        :param passwd_db: 数据库密码
        :param name_db: 数据库名称
        :param port_db: 端口号，整型数字
        :param link_type: 链接类型，用于输出数据是元祖还是字典，默认是字典，link_type=0
        :return:游标
        '''
        try:
            self.conn=MySQLdb.connect(host=host_db,user=user_db, passwd=passwd_db, db=name_db, port=port_db, charset='utf8')#创建数据库链接
            if link_type==0:
                self.cur=self.conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)#返回字典
            else:
                self.cur=self.conn.cursor()#返回元祖
        except MySQLdb.Error as e:
            print (u"创建数据库连接失败|Mysql Error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename = os.path.join(os.getcwd(), './log/syserror.log'),level = logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
    #定义单条数据操作，增删改
    def op_sql(self,condition):
        '''
        :param condition: sql语句,该通用方法可用来替代insertone，updateone，deleteone
        :return:字典形式
        '''
        try:
            self.cur.execute(condition)#执行sql语句
            self.conn.commit()
            result={'code':'0000','message':u'执行通用操作成功','data':[]}
        except MySQLdb.Error as e:
            result={'code':'9999','message':u'执行通用操作异常','data':[]}
            print (u"数据库错误|op_sql %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename = os.path.join(os.getcwd(), './log/syserror.log'),level = logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    #查询表中单条数据
    def selectOne(self,condition):
        '''
        :param condition: sql语句
        :return:字典形式的单条查询结果
        '''
        try:
            self.cur.execute(condition)
            results = self.cur.fetchone()#获取一条结果
            result={'code':'0000','message':u'执行单条查询操作成功','data':results}
        except MySQLdb.Error as e:
            result={'code':'9999','message':u'执行单条查询异常','data':[]}
            print (u"数据库错误|selectOne %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename = os.path.join(os.getcwd(), './log/syserror.log'),level = logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    #查询表中多条数据
    def selectAll(self,condition):
        '''
        :param condition: sql语句
        :return:字典形式的批量查询结果
        '''
        try:
            rows_affect=self.cur.execute(condition)
            if rows_affect>0:#查询结果返回数据数大于0
                self.cur.scroll(0, mode='absolute') # 光标回到初始位置
                results = self.cur.fetchall()#返回游标中所有结果
                result={'code':'0000','message':u'执行批量查询操作成功','data':results}
            else:
                result={'code':'0000','message':u'执行批量查询操作成功','data':[]}
        except MySQLdb.Error as e:
            result={'code':'9999','message':u'执行批量查询异常','data':[]}
            print (u"数据库错误|selectAll %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename = os.path.join(os.getcwd(), './log/syserror.log'),level = logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    #定义表中插入多条数据操作
    def insertMore(self,condition,params):
        '''
        :param condition: insert语句
        :param params: insert数据，列表形式[('3','Tom','1 year 1 class','6'),('3','Jack','2 year 1 class','7'),]
        :return:字典形式的批量插入数据结果
        '''
        try:
            results=self.cur.executemany(condition,params)#返回插入的数据条数
            self.conn.commit()
            result={'code':'0000','message':u'执行批量查询操作成功','data':int(results)}
        except MySQLdb.Error as e:
            result={'code':'9999','message':u'执行批量查询异常','data':[]}
            print (u"数据库错误|insertMore %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename = os.path.join(os.getcwd(), './log/syserror.log'),level = logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result
    #数据库关闭
    def __del__(self):
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()
if __name__ == "__main__":
    test=operationdb_interface()#实例化类
    result=test.selectAll("select c.* from zw_m_config c inner join zw_m_sim_card_info s ON  s.id= c.sim_card_id  and s.simcard_number ='19966660022' and c.flag = 1")
    #result=test.insertMore("insert into config_total(key_config,value_config,status) values(%s,%s,%s)",[(1,1,1),(2,2,2)])
    if result['code']=='0000':
        print(result['data'])
    else:
        print(result['message'])