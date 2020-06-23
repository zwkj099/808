#coding=utf-8
from testlibrary import jctool
import time
import threading
import socket
import os
import struct

'''
1、目前文件名是写死的，对应的是前向碰撞报警的文件名称
2、支持中位协议
3、使用前需要配置图片路径
'''
jctool = jctool()
def attach_upload(ip,tp,res,mobile,attach,filepath,version,deviceid):

    """文件名（00_e1_e100_0_b87441129fb34ef8969fd0de2739d15e.jpg）转成16进制格式
     文件名称可修改，文件大小不要大于64kb
     """
    filename1 = os.path.basename(filepath)  #filename1为原始文件名
    filename = tp.character_string(filename1) # filename转为16进制后的名称
    filename2 = tp.character_string1(filename1, 100)
    """filesize文件大小，filesize1文件大小转为16进制"""
    filesize = os.stat(filepath).st_size
    filesize1 = tp.to_hex(filesize, 8)
    filenamelen = str(hex(len(filename) / 2))[2:]  # 文件名长度
    if version == 1:
        """中位标准　9208:附件服务器 IP 地址长度(b)+附件服务器 IP 地址(str)+附件服务器端口（TCP,word）+附件服务器端口（UDP,word）+报警标识号 BYTE[21]+报警编号 BYTE[32]+预留 BYTE[16]"""
        iplenth = (int(res[36:38],16))*2 #获取9208指令中服务器地址长度字段
        port2 = (res[38 + iplenth:42+ iplenth]).replace(" ", "")#截取下发的1208中的端口号，并去掉空格
        port2=int(port2,16)  #转换为十进制
        alarmflag = res[42+iplenth:84+iplenth]  # 获取报警标识号
        alarm_number = res[84+iplenth:148+iplenth]

        """ 中位标准　附件信息列表:文件名称长度 BYTE+文件名称 STRING+多媒体类型 BYTE+文件大小 DWORD
        　组装1210指令消息体:终端手机号BCD[10]+报警标识号 BYTE[21]+报警编号 BYTE[32]+文件上报类型 BYTE+附件数量 BYTE+附件信息列表
        """
        attachlist = filenamelen + filename + attach + filesize1
        while len(mobile) < 20:
            mobile = '0' + mobile
        usual_body = mobile + alarmflag + alarm_number + '00' + '01' + attachlist  # 组装1210指令消息体
        head = tp.data_head(mobile, 4624, usual_body, 5, version)
        redata = tp.add_all(head + usual_body)

        link1 = tp.tcp_link(ip, port2)
        tp.send_data(link1, redata)
        tp.receive_data(link1)

        """中位标准　文件信息上传1211:文件名称长度 BYTE+文件名称 STRING+多媒体类型 BYTE+文件大小 DWORD"""
        fileinfo_head = tp.data_head(mobile, 4625, attachlist, 5, version)
        fileinfo = tp.add_all(fileinfo_head + attachlist)
        tp.send_data(link1, fileinfo)
        tp.receive_data(link1)

        """中位标准　文件数据上传-码流数据报文:帧头标识 DWORD+文件名称 BYTE[50]+数据偏移量 DWORD+数据长度 DWORD+数据体 BYTE[n]"""
        i = 0
        m = int(filesize // 65536)
        n = int(filesize % 65536)
        nsize = tp.to_hex(n, 8)
        picdata = open(filepath, 'rb')
        picbytes = picdata.read()

        streamhead = '30316364'
        if m == 0:
            data1 = streamhead + filename2 + '00000000' + filesize1
            data2 = tp.to_pack(data1)
            data = data2 + picbytes
            link1.send(data)
        else:
            for i in range(m + 1):
                dataoffset1 = i * 65536
                dataoffset2 = tp.to_hex(dataoffset1, 8)
                if m - i == 0:
                    # picdata.seek(dataoffset1,1)
                    data1 = streamhead + filename2 + dataoffset2 + nsize
                    data2 = tp.to_pack(data1)
                    data = data2 + picbytes[dataoffset1:dataoffset1 + filesize]
                    link1.send(data)
                    break
                elif m - i > 0:
                    data1 = streamhead + filename2 + dataoffset2 + '00010000'
                    data2 = tp.to_pack(data1)
                    data = data2 + picbytes[dataoffset1:dataoffset1 + 65536]
                    link1.send(data)
                    i += 1

        """文件上传完成指令1212:文件名称长度 BYTE+文件名称 STRING+文件类型 BYTE+文件大小 DWORD"""
        # usual_body = filenamelen + filename + '00' + filesize1  #图片
        usual_body = filenamelen + filename + attach + filesize1
        head = tp.data_head(mobile, 4626, usual_body, 5, version)
        flishdata = tp.add_all(head + usual_body)
        tp.send_data(link1, flishdata)
        tp.receive_data(link1)
        tp.close(link1)

    else:
        """冀标　9208:附件服务器 IP 地址长度(b)+附件服务器 IP 地址(str)+附件服务器端口（TCP,word）+附件服务器端口（UDP,word）+报警标识号BYTE[16]+报警编号 BYTE[32]+预留 BYTE[16]"""
        iplenth = (int(res[26:28],16))*2 #获取9208指令中服务器地址长度字段
        port2 = (res[28 + iplenth:32+ iplenth]).replace(" ", "")#截取下发的1208中的端口号，并去掉空格
        port2=int(port2,16)  ##转换为十进制
        alarmflag = res[36+iplenth:68+iplenth]  # 获取报警标识号
        alarm_number = res[68+iplenth:132+iplenth]

        """ 冀标　附件信息列表:文件名称长度 BYTE+文件名称 STRING+文件大小 DWORD
        　组装1210指令消息体:终端 ID BYTE[7]+报警标识号 BYTE[16]+报警编号 BYTE[32]+信息类型 BYTE+附件数量 BYTE+附件信息列表
        """
        attachlist = filenamelen + filename + filesize1
        usual_body = jctool.get_id(deviceid) + alarmflag + alarm_number + attach + '01' + attachlist

        head = tp.data_head(mobile, 4624, usual_body, 5, version)
        redata = tp.add_all(head + usual_body)

        link1 = tp.tcp_link(ip, port2)
        tp.send_data(link1,redata)
        tp.receive_data(link1)

        """冀标1211:文件名称长度 BYTE+文件名称 STRING+文件类型 BYTE+文件大小 DWORD"""
        attachlist = filenamelen + filename +attach+ filesize1
        fileinfo_head = tp.data_head(mobile, 4625, attachlist, 5, version)
        fileinfo = tp.add_all(fileinfo_head + attachlist)
        tp.send_data(link1, fileinfo)
        tp.receive_data(link1)

        """冀标　文件数据上传-码流数据报文:帧头标识 DWORD+文件名称 BYTE[50]+数据偏移量 DWORD+数据长度 DWORD+数据体 BYTE[n]"""
        i = 0
        m = int(filesize // 65536)
        n = int(filesize % 65536)
        nsize = tp.to_hex(n,8)
        picdata = open(filepath, 'rb')
        picbytes = picdata.read()

        streamhead = '30316364'
        if m == 0:
            data1 = streamhead + filename2 + '00000000' + filesize1 #缺少数据长度？？？
            data2 = tp.to_pack(data1)
            data = data2 + picbytes
            link1.send(data)
        else:
            for i in range(m+1):
                dataoffset1 = i * 65536
                dataoffset2 = tp.to_hex(dataoffset1, 8)
                if m - i == 0:
                    # picdata.seek(dataoffset1,1)
                    data1 = streamhead + filename2 + dataoffset2 + nsize
                    data2 = tp.to_pack(data1)
                    data = data2 + picbytes[dataoffset1:dataoffset1 + filesize]
                    link1.send(data)
                    break
                elif m - i > 0:
                    data1 = streamhead + filename2 + dataoffset2 + '00010000'
                    data2 = tp.to_pack(data1)
                    data = data2 + picbytes[dataoffset1:dataoffset1 + 65536]
                    link1.send(data)
                    i += 1

        """冀标 文件上传完成指令1212:文件名称长度BYTE+文件名称STRING+文件类型BYTE+文件大小DWORD"""
        usual_body = filenamelen + filename + attach + filesize1
        head = tp.data_head(mobile, 4626, usual_body, 5, version)
        flishdata = tp .add_all(head + usual_body)
        tp.send_data(link1,flishdata)
        tp.receive_data(link1)
        tp.close(link1)
        """文件上传完成消息应答9212 :文件名称长度 BYTE+文件名称 STRING+文件类型 BYTE+上传结果 BYTE(0x00完成)+补传数据包数量BYTE(无补传为0)+补传数据包列表"""



