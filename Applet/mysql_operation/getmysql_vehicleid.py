#encoding:utf8
from db_operation.mysql_connect import Mysql

def get_vehicleid(host,user,pwd,db,vnum):
    """
    :param host: mysql ip
    :param user:登录名
    :param pwd:密码
    :param db:数据库名
    :param vnum:监控对象名称
    :return:车辆id
    """
    # 打开数据库连接
    # mysql_test = Mysql(host,3306,user,pwd,db,vnum)
    # sql = "select id from zw_m_vehicle_info where brand ="+"'"+vnum+"'"
    # result = mysql_test.query(sql)
    # # print result[0][0]
    # return result[0][0]

#     for res in result:
#         print res[0]
#
# get_vehicleid('192.168.24.142' ,'root' ,'Zwkj@123Mysql' ,'clbs',u'桂AA001')
