# -*- coding: utf-8 -*-
import testlibrary
tp=testlibrary.testlibrary()

def f3_body(AD,Oil,high):
    '''组装F3附加信息，目前只实现了油量
                :param AD: 油量AD值
                :param Oil: 油量值
                :param high: 液位高度
                :param returnr:返回F3油量信息
                '''
    F3_body = tp.add_yw(65,0,AD,300,310,0,0,Oil,1,high)
    return tp.add_f3_data(1, F3_body)