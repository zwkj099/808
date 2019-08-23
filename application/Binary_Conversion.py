# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Binary_conver(object):
    def __init__(self):
        pass
    def hex_to_dec(self,data):
        #data 是十六进制字符串
        return int(data,16)
