# coding=utf-8

from mytool import mytool
from jctool import jctool
from extool import analysis_data
from opmysql import operationdb_interface

__version__ = '3.3'
"""
修改：
报文组装方式还原，中间不要空格，仅打印日志时，转化为每byte后加空格的格式
新增：
新增OBD行程数据组装相关方法
"""
class testlibrary(mytool,jctool,analysis_data,operationdb_interface):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    def __init__(self):
        operationdb_interface.__init__(self,host_db='192.168.24.142',user_db='root',passwd_db='Zwkj@123Mysql',name_db='clbs',port_db=3306,link_type=0)

    def __del__(self):
        operationdb_interface.__del__(self)


