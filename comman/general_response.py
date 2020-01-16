# -*- coding: utf-8 -*-
import testlibrary
tp=testlibrary.testlibrary()

#组装响应报文body
def get_usyal_body(id,ac,reno="00"):
    body=ac+id+reno
    return body

#通用应答
def Usual(link,mobile,id,answer_number,reno):
    '''组装通用应答报文，并发送
           :param link: 连接
           :param mobile: 手机号
           :param id: 应答消息ID
           :param answer_number: 应答流水号
           :param reno:应答结果
           '''

    usual_body = get_usyal_body(id, answer_number, reno)
    usual_head = tp.data_head(mobile, 1, usual_body, 5)
    result = tp.add_all(usual_head + usual_body)
    res = tp.send_data(link, result)
    return res

