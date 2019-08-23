# -*- coding: utf-8 -*-
import testlibrary
tp=testlibrary.testlibrary()

#0900应答
def Answer_0900(link,mobile,sensor,answer_number,reno):
    '''组装0900报文，并发送
            :param link: 连接
            :param mobile: 手机号
            :param sensor: 传感器ID
            :param answer_number: 应答流水号
            :param reno:应答结果
            '''
    usual_body = "F301"+ sensor +"03" + answer_number + reno
    usual_head = tp.data_head(mobile, 2304, usual_body, 5)
    result = tp.add_all(usual_head + usual_body)
    res = tp.send_data(link, result)
    return res
