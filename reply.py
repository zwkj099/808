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
        rlist = ["8104","8103","8106", "8107","8201", "8900", "8001"]
        if id not in rlist:
            usual_body = get_usyal_body(id, answer_number, reno)
            usual_head = tp.data_head(mobile, 1, usual_body, 5,version)
            usual_redata = tp.add_all(usual_head + usual_body)
            tp.send_data(link, usual_redata)

        # 平台下发指令8106，查询指定终端参数
        elif id == "8106":
            search_body = get_loadres_body(tp,res,answer_number,version)
            search_head = tp.data_head(mobile, 260, search_body, 5,version)
            search_data = tp.add_all(search_head + search_body)
            tp.send_data(link, search_data)
        # 平台下发指令8104，查询全部终端参数
        elif id == "8104":
            search_body = answer_number+"1A00000001040000003C0000001005434D4E455400000011000000001200000000130C3131332E3230342E352E3538000000180400001B3F0000002004000000000000002704000000140000002904000000140000002C040000006400000030040000000F00000055040000006400000056040000000A0000005704000038400000005904000004B00000005B0200320000005C0207080000005E02001E0000008004000000000000008102002C0000008202012F0000008308D4C14238363636360000008401010000009001030000F44F380000000000000000000002000014006E000000000000000000000000000000000000000000000000000000000000000000000000000000000000F4503800000000000000000000001432320A0000000000000000000000000000000000000000000000000000000000000000000000000000000000"
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
            # 获取下发的透传类型
            if version==0:
                typ = res[26:28]
                sensor = res[34:36]
            elif version==1:
                typ = res[36:38]
                sensor = res[40:42]
            # 透传类型为Ｆ３协议时，组装应答数据
            if typ=="F6":
                usual_body = "F301" + sensor + "03" + answer_number + reno
            else:# 透传类型为非Ｆ３协议时，组装应答数据；实时监控的原始指令下发
                usual_body = typ+ "323034393338303233393834303233383430393332383432333432333432346F6F6F6F6FB0A2C0ADC9BDBFDABDB2B5C0C0EDC8F8BFCBBDA8B5B5C1A2BFA8313235393939313233343536373839313233343536373839313233343536373839313131313233343536373839313233343536373839313233343536373839313131"
            usual_head = tp.data_head(mobile, 2304, usual_body, 5,version)
            result = tp.add_all(usual_head + usual_body)
            tp.send_data(link, result)
        # 平台下发指令8103，传感器参数设置
        elif id == "8103":
            #先应答通用应答
            usual_body = get_usyal_body(id, answer_number, reno)
            usual_head = tp.data_head(mobile, 1, usual_body, 5,version)
            usual_redata = tp.add_all(usual_head + usual_body)
            tp.send_data(link, usual_redata)
            # 获取设置的ID，如果是带F3的ID，则通用应答后需要继续应答0900；根据版本确认是按2013-808格式应答，还是按2019-808格式应答
            if version==0:#2013-808格式
                if tp.to_int(res[28:34]) == 243:
                    sensor = res[34:36]
                    usual_body = "F301" + sensor + "03" + answer_number + reno
                    usual_head = tp.data_head(mobile, 2304, usual_body, 5,version)
                    result = tp.add_all(usual_head + usual_body)
                    tp.send_data(link, result)
            elif version==1:#2019-808格式
                if tp.to_int(res[38:44]) == 243:
                    sensor = res[44:46]
                    usual_body = "F301" + sensor + "03" + answer_number + reno
                    usual_head = tp.data_head(mobile, 2304, usual_body, 5,version)
                    result = tp.add_all(usual_head + usual_body)
                    tp.send_data(link, result)
         #短信平台私有协议，文本下发
        # elif id=="8300":
        #     tag = res[61:66] #获取下发的标识，确认下发的内容是什么，在进行对应应答
        #     #回应通用应答
        #     usual_body = get_usyal_body(id, answer_number, reno)
        #     usual_head = tp.data_head(mobile, 1, usual_body, 5, version)
        #     usual_redata = tp.add_all(usual_head + usual_body)
        #     tp.send_data(link, usual_redata)
        #     #判断应答内容,回应对应回应
        #     sim="#simID:13627667666*ID:7667666GPS:A*CSQ:20*CGR:1*VER:F200A-V2.5.5"
        #     if tag=="S10":
        #         usual_body =tag +"* ABCDEF"+sim
        #     elif tag=="F10":
        #         usual_body =tag+"*ABCDEF"
        #     elif tag=="S11":
        #         usual_body = tag+"*IP1*112.126.64.32*6975"+sim
        #     elif tag=="F11":
        #         usual_body = tag + "*IP1*112.126.64.32*6975"+sim
        #     elif tag=="S12":
        #         usual_body = tag + "*APN"+sim
        #     elif tag=="F12":
        #         pass
        #     elif tag=="S13":
        #         usual_body = tag + "*13627667666 * 7667666"+sim
        #     elif tag=="F13":
        #         pass
        #     elif tag=="S14":
        #         pass
        #     elif tag=="S15":
        #         pass
        #     elif tag=="S16":
        #         usual_body = tag + "*文件名;用户名;密码;IP地址;端口;路径"+sim
        #     elif tag=="S17":
        #         usual_body = tag + "*模式*参数" + sim
        #     elif tag=="F17":
        #         pass
        #     elif tag=="S18":
        #         usual_body = tag + "*休眠模式*是否上报位置信息*位置上报间隔*心跳上报间隔" + sim
        #     elif tag=="F18":
        #         pass
        #     elif tag=="S19":
        #         usual_body = tag + "*0#"
        #     elif tag=="F19":
        #         pass
        #     elif tag=="S20":
        #         usual_body = tag + "*IP1*112.126.64.32*端口号*SIM卡号*设备ID*车牌颜色" + sim
        #     elif tag=="F20":
        #         pass
        #     elif tag=="S21":
        #         usual_body = tag + "*车牌号*车牌颜色*VIN码" + sim
        #     elif tag=="F21":
        #         pass
        #     elif tag=="S22":
        #         usual_body = tag + "*总里程" + sim
        #     elif tag=="S23":
        #         usual_body = tag + "*电压值" + sim
        #     elif tag=="F23":
        #         pass
        #     elif tag=="S24":
        #         usual_body = tag + "*定位模式" + sim
        #     elif tag=="F24":
        #         pass
        #     elif tag=="S25":
        #         usual_body = tag + "*模式*阈值1*阈值2*阈值3" + sim
        #     elif tag=="F25":
        #         pass
        #     elif tag=="S26":
        #         usual_body = tag + "*距离阈值" + sim
        #     elif tag=="F26":
        #         pass
        #     #回应对应回应
        #     No="IP1"#从下发的内容中解析出来，IP1或IP2
        #     IP="112.126.64.32"#从下发的内容中解析出来
        #     port="6975"#从下发的内容中解析出来
        #     usual_body = "F50101" + "S11*"+No+"*"+IP+"*"+port+"#simID:13627667666*ID:7667666*GPS:A*CSQ:20*CGR:1*VER:F200A-V2.5.5" #设置上级平台
        #     usual_head = tp.data_head(mobile, 2304, usual_body, 5, version)
        #     result = tp.add_all(usual_head + usual_body)
        #     tp.send_data(link, result)

    except:
        pass
#组装响应报文body
def get_usyal_body(id,ac,reno="00"):
    body=ac+id+reno
    return body

#组装读取指令应答body
def get_loadres_body(tp,data,answer_number,version):
    #取得参数总数（可用于校验，未实现）
    total=data[26:28]
    #取得下发报文的流水号
    ac=answer_number#data[22:26]
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
    if version ==1:
        body=data[38:-4]
    elif version==0:
        body = data[28:-4]
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
        elif id == "0000F641":#油量标定数组
            da=id+"75000000CA0000005B00000194000000B70000025E00000112000003280000016D000003F2000001C9000004BC00000224000005860000027F00000650000002DA0000071A00000336000007E400000391000008AE000003EC000009780000044800000A42000004A300000B0C000004FE00000BD60000055A00000CA0000005B500000D6A0000061000000E340000066C00000EFE000006C700000FC800000722FFFFFFFFFFFFFFFF247E"
        # 高精度硬件参数读取0X4F0和x50，按0X4F0和x50设置的协议格式上传
        elif id == "0000F450" or id =="0000F44F":
            da0 = "0000F44F" + "38000000000000000000000000"+"101020203030"+"0000000000000000000000000000000000000000000000000000000000000000000000000000"
            da1="0000F450" + "15000000000000000000000000"+"323232"+"000000000000"
            da=da0+da1
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
    resbody=ac+ tp.to_hex(x,2)+parbody
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