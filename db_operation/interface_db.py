# -*- coding: utf-8 -*-

'''
Created on 2019-8-18

@author: Administrator
'''

class interface_db(object):
    
    def __init__(self):
        pass
    def db_opertation(self,tp,testlibrary):
        resul = tp.selectAll("select c.* from zw_m_config c inner join zw_m_sim_card_info s ON  s.id= c.sim_card_id  and s.simcard_number ='19966660022' and c.flag = 1")
     
        base_operationdb_interface = testlibrary.opmysql.operationdb_interface()  # 实例化接口测试数据库操作类
        resul=base_operationdb_interface.selectAll("select c.* from zw_m_config c inner join zw_m_sim_card_info s ON  s.id= c.sim_card_id  and s.simcard_number ='19966660022' and c.flag = 1")
        print "CCC",resul


