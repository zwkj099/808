# -*- coding: utf-8 -*-
#应答脚本
import time
import threading
import thread
import testlibrary
import random
import re
import datetime
#tp=testlibrary.testlibrary()

"""
1.持续发送位置，心跳报文
2.监听接收
3.收到平台报文后，判断是否需要应答
4.需要应答时组装应答报文发送
5.应答结果配置设置
6.多线程
"""

def reply(tp,link,res,mobile,id,answer_number, reno,version=0):
    try:
        #reno = "00"
        """
        x += 1
        if x%5==1:
            reno="01"#失败
        elif x%5==2:
            reno="02"#消息有误
        elif x%5==3:
            reno="03"#不支持
        elif x%5==4:
            time.sleep(3)#超时
        else:
            pass
        print "第%d次应答%s" % (x, reno)
        """
        rlist = ["8103", "8106", "8107","8201", "8900", "8001"]
        if id not in rlist:
            usual_body = get_usyal_body(id, answer_number, reno)
            usual_head = tp.data_head(mobile, 1, usual_body, 5,version)
            usual_redata = tp.add_all(usual_head + usual_body)
            tp.send_data(link, usual_redata)

        # 平台下发指令8106，查询指定终端参数
        elif id == "8106":
            search_body = get_loadres_body(res)
            search_head = tp.data_head(mobile, 260, search_body, 5,version)
            search_data = tp.add_all(search_head + search_body)
            tp.send_data(link, search_data)

        # 平台下发指令8107，查询终端属性
        elif id == "8107":
            search2_body = get_0107body(version)
            search2_head = tp.data_head(mobile, 263, search2_body, 5,version)
            search2_data = tp.add_all(search2_head + search2_body)
            print search2_data
            tp.send_data(link, search2_data)

            # 平台下发指令8900,油量标定数组
        elif id == "8900":
            usual_body = get_usyal_body(id, answer_number, reno)
            usual_head = tp.data_head(mobile, 1, usual_body, 5, version)
            usual_redata = tp.add_all(usual_head + usual_body)
            tp.send_data(link, usual_redata)
            # Answer_0900(link, mobile, res[34:36], answer_number, reno)  # 应答0900
            if version==0:
                typ = res[30:32]
            elif version==1:
                typ = res[36:38]
                sensor = res[40:42]
            if typ=="F6":
                usual_body = "F301" + sensor + "03" + answer_number + reno
            else:
                usual_body = typ+ "550205"
            usual_head = tp.data_head(mobile, 2304, usual_body, 5,version)
            result = tp.add_all(usual_head + usual_body)
            tp.send_data(link, result)
        # 平台下发指令8103，传感器参数设置
        elif id == "8103":
            # Usual(link, mobile, id, answer_number, reno)  # 应答通用应答
            usual_body = get_usyal_body(id, answer_number, reno)
            usual_head = tp.data_head(mobile, 1, usual_body, 5,version)
            usual_redata = tp.add_all(usual_head + usual_body)
            tp.send_data(link, usual_redata)
            if tp.to_int(res[28:34]) == 243:  # 获取设置的ID，如果是带F3的ID，则通用应答后需要继续应答0900
                # Answer_0900(link,mobile, res[34:36], answer_number, reno)
                sensor = res[34:36]
                usual_body = "F301" + sensor + "03" + answer_number + reno
                usual_head = tp.data_head(mobile, 2304, usual_body, 5,version)
                result = tp.add_all(usual_head + usual_body)
                tp.send_data(link, result)

    except:
        pass
#组装响应报文body
def get_usyal_body(id,ac,reno="00"):
    body=ac+id+reno
    return body

#组装读取指令应答body
def get_loadres_body(data):
    #取得参数总数（可用于校验，未实现）
    total=data[26:28]
    #取得下发报文的流水号
    ac=data[22:26]
    #string类型id添加在这里
    list1=["00000083","00000049","00000048","00000040","00000041","00000042","00000043",
           "00000044","0000001D","0000001A","00000010","00000011","00000012","00000013",
           "00000014","00000015","00000016","00000017"]
    #byte类型id添加在这里
    list2=["00000084","00000090","00000091","00000092","00000094"]
    #word类型id添加到这里
    list3=["00000101","00000103","00000081","00000082","0000005B","0000005C","0000005D",
           "0000005E","00000031"]
    #byte[8]类型添加到这里
    list4=["00000110"]
    #DWORD类型放在else里面
    body=data[28:-4]
    print "get_loadres_body(data)", body
    parbody=""
    x=0
    while body:
        id=body[0:8]
        print id
        body=body[8:]
        #此处将id和值组装起来，可以添加if条件来特殊处理某些参数，也可以修改一些默认参数、或去掉一些应答
        #下面组装为id+长度+值
        if id =="0000F901" or id =="0000F902" or id =="0000F903":
            da=id+"1904"+"0001050101010005"+"010106020202FFFF"+"020207020303FFFF"+"03020702030300FF"
        elif id == "0000F904":
            da=id+"0401020401"
        elif id == "0000F905":
            da=id+"0A01000201030204030600"
        elif id == "0000F906":
            da=id+"070A000102030000000000000A00010203000000000000"
        elif id == "0000F641":
            da=id+"150000003A000000010000007500000005000000B00000000A000000EA0000001000000124000000160000015F0000001D0000019A00000023000001D40000002B0000020E00000032000002490000003A0000028300000042000002BE0000004A000002F80000005100000333000000580000036E00000060000003A800000066000003E30000006B0000041D0000007000000458000000750000049200000078FFFFFFFFFFFFFFFF247E"
        elif id in list1:
            da=id+"0474657374"
        elif id in list2:
            da=id+"0101"
        elif id in list3:
            da=id+"020101"
        elif id in list4:
            da=id+"080101010101010101"
        else:
            da=id+"0400000001"
        x+=1
        parbody=parbody+da
    resbody=ac+tp.to_hex(x,2)+parbody
    return resbody


#组装传感器拓展查询基本信息应答报文body
def get_searchsenior_body(data):
    ac=data[22:26]
    sid=data[-6:-4]
    print "this is sid",sid
    """
    数据长度+公司名称长度+名称+产品代码长度+代码+硬件版本号长度+硬件版本号+
    软件版本号长度+版本号+设备id长度+设备id+客户代码长度+客户代码
    """
    d=ac+"01"+"0000F8"+sid
    s="13"+"01"+"31"+"01"+"31"+"01"+"31"+\
      "01"+"31"+"08"+"3132333435363131"+"01"+"35"
    body=d+s
    return body
#组装0107body
def get_0107body(version):
    """
    终端类型（word）+制造商id（b5）+终端型号（b20）+终端id（b7）+sim卡iddid（bcd10）
    +终端硬件版本长度（b）+硬件版本号+终端固件版本长度（b）+固件版本号+GNSS模块（b）
    +通信模块（b）
    """
    if version==0:
        parm = "0008" + "3131323334" + "3131323334313132333431313233343131323334" + \
               "31313233343639"+"31313233343131323334"+"08312E382E352E3132"+"08312E382E352E3132"+"08"+"08"
    elif version==1:
        parm="0008"+"3130303030303131323334"+"313132333431313233343131323334313132333434343435353535353538"+\
             "313132333431313233343131323334313132333434343435353535353538"+"31313233343131323334"+"08312E382E352E3132"+\
             "08312E382E352E3132"+"08"+"08"
    return parm
#通用应答
# def Usual(link,mobile,id,answer_number,reno):
#     '''组装通用应答报文，并发送
#            :param link: 连接
#            :param mobile: 手机号
#            :param id: 应答消息ID
#            :param answer_number: 应答流水号
#            :param reno:应答结果
#            '''
#     usual_body = get_usyal_body(id, answer_number, reno)
#     usual_head = tp.data_head(mobile, 1, usual_body, 5)
#     result = tp.add_all(usual_head + usual_body)
#     tp.send_data(link, result)

#0900应答
# def Answer_0900(link,mobile,sensor,answer_number,reno):
#     '''组装0900报文，并发送
#             :param link: 连接
#             :param mobile: 手机号
#             :param sensor: 传感器ID
#             :param answer_number: 应答流水号
#             :param reno:应答结果
#             '''
#     usual_body = "F301"+ sensor +"03" + answer_number + reno
#     usual_head = tp.data_head(mobile, 2304, usual_body, 5)
#     result = tp.add_all(usual_head + usual_body)
#     tp.send_data(link, result)