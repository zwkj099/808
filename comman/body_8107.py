# -*- coding: utf-8 -*-
import testlibrary
tp=testlibrary.testlibrary()

#组装0107body
def get_0107body():
    """
    z终端类型（word）+制造商id（b5）+终端型号（b20）+终端id（b7）+sim卡iddid（bcd10）
    +终端硬件版本长度（b）+硬件版本号+终端固件版本长度（b）+固件版本号+GNSS模块（b）
    +通信模块（b）
    """
    parm="0008"+"3131323334"+"3131323334313132333431313233343131323334"+\
         "31313233343639"+"31313233343131323334"+"08312E382E352E3132"+\
         "08312E382E352E3132"+"08"+"08"
    return parm