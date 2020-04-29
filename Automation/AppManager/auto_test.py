# -*- coding: utf-8 -*-


import re
# 应答脚本
import time

import testlibrary

tp=testlibrary.testlibrary()
import application
# from Automation.AppManager import application
from selenium import webdriver
app = application.application()
import win32api
import win32con
import TAException
import os


__funclist         = []
__argslist         = []
__func             = None
testinfo           = {}

def readtestfile():
    from xml.dom import minidom
    try:
        testfile = "./Automation/AppManager/appconfig/testconfig.xml"
        dom = minidom.parse(testfile)
        tmp = dom.getElementsByTagName("TestList")
        if tmp != []:
            if tmp[0].getElementsByTagName("Test") != []:
                testlist =  tmp[0].getElementsByTagName("Test")
                for item in testlist:
                    func = ""
                    arg  = ""
                    try:
                        func, arg = item.childNodes[0].data.split(",",1)
                    except:
                        func = item.childNodes[0].data
                        arg  = ""
                    __funclist.append(func)
                    __argslist.append(arg)
        keyvalueslst = dom.getElementsByTagName("KeyValues")
        for keyvalue in keyvalueslst:
            key   = keyvalue.getElementsByTagName("Key")[0].childNodes[0].data
            value = keyvalue.getElementsByTagName("Value")[0].childNodes[0].data
            testinfo[key] = value
    except:
            raise TAException.taexception(3,"\n"+testfile+" format is not correct\n","TEST_AUTOMATION_ERROR")

    return [__funclist,__argslist,testinfo]

def dynamicimport(__funclist):
    import sys
    sys.path.append(testinfo['TestLibPath'])
    del sys
    print __funclist
    try:
        __func = map(__import__, __funclist)
    except ImportError, err:
        print err
        raise TAException.taexception(4,"import module error:\n"+err.message,"TEST_AUTOMATION_ERROR")
    return __func



def __createlogfile(logname,logfile):
    try:
#         print logname
        if not os.path.isdir("c:\\TALOG"):
            os.mkdir("c:\\TALOG")
        logfile = file("c:\\TALOG\\" + logname, "a+")

    except:
        raise TAException.taexception(2,"Fail to create log file: \n" + "c:\\TALOG\\" + logname,"CREATE_LOG_FILE_ERROR")
    return logfile

def __renamelog(logname,testresult):
    oldfile = "c:\\TALOG\\" + logname
    logname = logname.replace(".log","[" + testresult + "].log")
    for i in range(5):
        try:
            os.rename(oldfile,"c:\\TALOG\\"+logname)
            break
        except:
            continue

def __logtofile(__logfile,buf):

    try:
        __logfile.write(buf)
        __logfile.write("\n")
        __logfile.flush()
    except:
        raise TAException.taexception(2,"write log to file error","WRITE_LOG_ERROR")


def auto_test(tp,link,mobile,vnum):

    # browser = webdriver.Chrome()
    browser = webdriver.Firefox()
    url='http://192.168.24.142:8080/clbs/login'
    #登录网页
    __logname =time.strftime("%Y/%m/%d %X", time.localtime()).replace("/","_").replace(":","_")+".log"#'2019_07_17 17_44_25'
    __logfile = None
    __logfile=__createlogfile(__logname,__logfile)

    username='ydy'
    password='123456'
    app.login(url,browser,username,password)
    __logtofile(__logfile, "login success!\nusername:"+username+"\nurl:"+url+"\n")
    __funclist,__argslist,testinfo=readtestfile()
    __func=dynamicimport(__funclist)

    testresult = "PASS"
    try:
        filedic={"labor":u"工时管理","load":u"载重管理","mileage":u"里程监测","obd":u"OBD管理","oil_test":u"油量管理","oilwear":u"油耗管理",\
                  "polling":u"外设轮询","psi":u"胎压监测","reversible":u"正反转管理","temp":u"温度监测","wetness":u"湿度管理"}
        filename=""
        for test in range(len(__func)):
            for key,value in filedic.items():
                if str(__func[test].__name__).find(key)!=-1:
                    filename=value
                    break
            __logtofile(__logfile,"***********************************************************************************************\n\
************************************"+filename+" "+str(__func[test].__name__)+".py*****************************************\n\
***********************************************************************************************\n")
            try:
                __func[test].main(browser,__argslist[test],testinfo,tp,link,app,mobile,vnum,__logfile,__logtofile)
            except Exception as e:
                print e

    except TAException.taexception, errobj:
        testresult      = "FAIL"
        __logtofile(__logfile,errobj.errmsg)
    except TAException.test_fail, errobj:
        testresult      = "FAIL"
        __logtofile(__logfile,errobj.errmsg)

    except Exception as e:
        print e
        testresult      = "FAIL"
        __logtofile(__logfile,e)
    finally:
        fail_list=[]
        pass_list=[]

        with open("c:\\TALOG\\" + __logname,'r') as f:
            data = f.readlines()
            for line in data:
                if re.findall(r'test.*pass', line.strip(" "), re.I)!=[] and line.strip(" ") not in pass_list :
                    pass_list.append(line)

                elif re.findall(r'test.*fail', line.strip(" "), re.I)!=[] and line.strip(" ") not in fail_list:
                    fail_list.append(line)

        print pass_list
        print fail_list
        if pass_list!=[]:
            __logtofile(__logfile,"Test result: \nTotal pass:"+str(len(pass_list))+"\n")

        if fail_list!=[]:
            __logtofile(__logfile,  "Total fail:"+str(len(fail_list))+"\n")


        if fail_list!=[]:
            testresult = "FAIL"
            __logtofile(__logfile, "FAIL module:\n")
            for k in fail_list:
                __logtofile(__logfile, str(k))

        __logfile.close()
        __renamelog(__logname,testresult)

    win32api.MessageBox(0, "All test complete !", "Test Result",win32con.MB_OK)
    browser.quit()


