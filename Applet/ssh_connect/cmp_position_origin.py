# -*- coding:utf-8 -*-

import paramiko
import re
import json

def cmp_pos(host,user,pwd,simcard,vehicle_hex):
    """
    :param host: ssh服务器ip
    :param user: 登录名
    :param pwd: 密码
    :param simcard: 车辆simcard
    :param vnum: 车辆名称
    :return: 返回比对结果True or False
    """
    ssh = paramiko.SSHClient()  # 创建SSH对象
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
    ssh.connect(hostname=host, port=22, username=user, password=pwd)  # 连接服务器
    """
    获取808 0200最后一条数据，并读取发送的时间
    """
    if len(simcard)%2!=0:
        simcard1 ="0"+simcard
    pattern = re.compile('.{2}')
    simcard_new=(' '.join(pattern.findall(simcard1)))

    res_808 =''
    i=0
    while (res_808=='' or res_808.find('7E 02 00')==-1)and i<30:
        stdin, stdout, stderr = ssh.exec_command(
            "tail -n 100 /home/f3/protocol/info.log |grep '%s'" %simcard_new)  # 执行命令并获取命令结果
        # stdin为输入的命令
        # stdout为命令返回的结果
        # stderr为命令错误时返回的结果
        res_808, err = stdout.read(), stderr.read()
        result = res_808 if res_808 else err
        i+=1

    if i>=30: ##查找30次没有查到跳出循环
        print "Loop through 30 times with no result"
    print "808 0200:\n"+result

    ## 取出808 0200最后一条值
    start =[m.start() for m in re.finditer('7E 02 00',result)][-1]
    end = result.find('INFO',start)
    data_808 = result[start:end]
    send_time = re.findall('\d+:\d+:\d+',result)[0] ##0200发送开始时间，为了找出接收时间比这个时间晚


    """
    读取809 前100条（接收Kafka-转发消息）的信息，并且最后一条消息接收的时间要比0200发送的时间晚
    """

    rec_time =''
    res_809 =''
    j=0
    while (res_809=='' or (int(rec_time[:-4].replace(":",""))<int(send_time.replace(":",""))) or result1.find('gps')==-1)and j<30: ##有时候接收到的json没有gps
        stdin, stdout, stderr = ssh.exec_command(
            "tail -n 100 /home/f3/809/info.log |grep '%s'"%vehicle_hex)  # 执行命令并获取命令结果
        res_809, err = stdout.read(), stderr.read()
        result1 = res_809 if res_809 else err

        if res_809!='':
            rec_time = re.findall('\d+:\d+:\d+\.\d+',result1)[-1]
        j+=1
    if j>=30:##查找30次没有查到跳出循环
        print "Loop through 30 times with no result"
    print "809 data info\n"+result1
    ssh.close()  # 关闭连接

    """
    解析808 0200上传数据，把要对比的数据放到列表send_data中
    """

    ##解析808数据
    data_808 = data_808.replace(" ","")
    start = data_808.find(simcard)+len(simcard)+4
    end = start+8

    melstart=0
    melend=0
    if data_808.find("0104",end+48):
        melstart= data_808.find("0104",end+48)+4
        melend =melstart+8

    recorder_speed_start =0
    recorder_speed_end =0
    if data_808.find("0302",melend):
        recorder_speed_start= data_808.find("0302",melend)+4
        recorder_speed_end =recorder_speed_start+4

    #起始位置到终止位置，hex表示不转换，float表示转为浮点数，int表示直接转为整数，否则由16进制转为十进制
    data_list =[(start,end),(end,end+8),(end+8,end+16),(end+16,end+24),(end+24,end+28),(end+28,end+32),(end+32,end+36),\
                (end+36,end+38,"hex"),(end+38,end+40,"int"),(end+40,end+42,"int"),(end+42,end+44,"int"),\
                (end+44,end+46,"int"),(end+46,end+48,"int"),(melstart,melend),(recorder_speed_start,recorder_speed_end)]

    from Automation.AppManager import application
    app = application.application()
    #获取解析后的值
    send_data = app.data_convert(data_list,data_808)
    #数据转换
    send_data[0] = 1 if send_data[0]!=0 else 0  #如果不为0，则显示1，报警，否则显示0，不报警
    send_data[-2] = int(send_data[-2]*0.1)  #里程小数往左移一位取整，不懂平台有没有做四舍五入？

    print send_data

    data_title=["alarm","status","latitude","longtitude","height","speed","direction","year","month",\
                              "day","hour","minute","second","gps_mile","recorder_speed"]

    """
    取出809最后一条消息，并且将要比对的数据放到列表 rec_data中
    """

    ##取出809_接收Kafka-转发消息 最后一条值
    start1 =[m.start() for m in re.finditer('T809-主链路-Encode:5B',result1)][-1]
    data_809 =result1[start1+len('T809-主链路-Encode:'):].replace(" ","")
    print data_809
    l= len(data_809)
    rec_list =[(l-15,l-7),(l-23,l-15),(128,136),(120,128),(156,160),(136,140),(152,156),\
                (110,114),(108,110),(106,108),(114,116),(116,118),(118,120),(144,152),(140,144)]
    # 获取解析后的值
    rec_data = app.data_convert(rec_list, data_809)
    rec_data[7]=str(rec_data[7])[2:] #年份取后面两位

    print rec_data

    # 数据结果进行比对

    k=True
    for j in range(len(send_data)):
        if str(send_data[j]).strip() != str(rec_data[j]).strip():
            print "error:[" + data_title[j] + " ]  send data: " + str(send_data[j]) + "   receive data: " + str(
                rec_data[j]) + " not match"
            k=False


    return k


# cmp_pos('192.168.24.142','root','zwkj@ZWLBS.com','14875300001','30 30 30 30 33')




