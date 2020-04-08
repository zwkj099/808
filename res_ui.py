# -*- coding: utf-8 -*-
import time
import testlibrary
import threading
tp=testlibrary.testlibrary()
from PyQt4 import QtGui, QtCore, uic
import sys
#读取ui文件

#wind, base = uic.loadUiType('C:Python27/Lib/site-packages/PyQt4/test.ui')
wind, base = uic.loadUiType('res1.ui')
class fwindow(wind, base):
    #窗口显示
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        #self.setWindowIcon(QtGui.QIcon(ico))
        self.set()
    def set(self):
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.help)
        self.show()
    def start1(self):
        reno=self.comboBox.currentIndex()
        print reno
    def start(self):
        self.ip=unicode(self.lineEdit.text()).encode("utf-8")
        self.mobile=unicode(self.lineEdit_2.text()).encode("utf-8")
        self.number=unicode(self.lineEdit_3.text()).encode("utf-8")
        mobile=int(self.mobile)
        number=int(self.number)
        endmobile=mobile+number
        for i in range(mobile,endmobile):
            r = threading.Thread(target=self.send,args=(self.ip,i))
            r.start()
    def send(self,ip,mobile):
        time.sleep(1)
        ip=str(ip)
        port="6975"
        mobile=str(mobile)
        deviceid="1234567"
        vnum="测SSR999"
        link=tp.tcp_link(ip,port)
        zcbody=tp.data_zc_body(deviceid,vnum)
        zchead=tp.data_head(mobile,256,zcbody,1)
        zcdata=tp.add_all((zchead+zcbody))
        tp.send_data(link,zcdata)
        zcres=tp.receive_data(link)
        time.sleep(1)
        jqbody=tp.data_jq_body(zcres)
        jqhead=tp.data_head(mobile,258,jqbody,2)
        jqdata=tp.add_all((jqhead+jqbody))
        time.sleep(1)
        tp.send_data(link,jqdata)
        jqres=tp.receive_data(link)
        time.sleep(1)
        gpsbody=tp.data_gps_body(0,0,106.555555,29.000000,500,0,0,100)
        gpsbody=gpsbody
        gpshead=tp.data_head(mobile,512,gpsbody,3)
        gpsdata=tp.add_all(gpshead+gpsbody)
        tp.send_data(link,gpsdata)
        res=tp.receive_data(link)
        res=tp.dd(res)
        x=0
        while True:
            y=0
            while True:
                y+=1
                if y>=30:
                    y=0
                    heartbeat_body=""
                    heartbeat_head=tp.data_head(mobile,2,heartbeat_body)
                    heartbeat_data=tp.add_all(heartbeat_head)
                    tp.send_data(link,heartbeat_data)
                    tp.receive_data(link)
                else:
                    try:
                        res=tp.receive_data(link)
                        res=tp.dd(res)
                        if res[3:8]=="80 01":
                            pass
                        else:
                            reno=self.comboBox.currentIndex()
                            if int(reno)==4:
                                pass
                            else:
                                reno=tp.to_hex(reno,2)
                                print reno
                                id = res[2:6]
                                ac = res[22:26]
                                usual_body =ac+id+reno
                                # print usual_body
                                usual_head = tp.data_head(mobile, 1, usual_body, 5)
                                usual_redata = tp.add_all(usual_head + usual_body)
                                tp.send_data(link, usual_redata)
                                tp.receive_data(link)
                    except:
                        pass
        tp.close(link)
    def help(self):
        reply = QtGui.QMessageBox.question(self, 'HELP', u'输入ID地址和手机号后，点击start，即可自动完成上线。\n'
                                                         u'递增设置会根据设置数字，手机号自动递增上线。\n'
                                                         u'应答设置会实时生效。\n'
                                                         u'P.S.可以安装pyqt修改ui文件，如果你有更好的idea。',
                                           )
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    F=QtGui.QWidget()
    main=fwindow()
    sys.exit(app.exec_())