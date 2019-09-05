# -*- coding: utf-8 -*-
import testlibrary
tp=testlibrary.testlibrary()

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