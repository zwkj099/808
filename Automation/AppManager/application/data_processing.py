# -*- coding: utf-8 -*-
import re
import sys

# from Automation.AppManager import application

reload(sys)
sys.setdefaultencoding('utf8')

class data_processing(object):

    def __init__(self):
        pass

    def data_convert(self,data,res):
        from Automation.AppManager import application
        app = application.application()
        rec_data=None
        if isinstance(data, list):
            rec_data=[]
            for da in data:
                if len(da)==2:
                    rec_data.append(app.hex_to_dec(res[da[0]:da[1]]))
                elif len(da)==3:
                    if da[2]=="hex":
                        rec_data.append(res[da[0]:da[1]])
                    elif da[2]=="int":
                        rec_data.append(int(res[da[0]:da[1]]))##直接转换为整数
                elif len(da)==4:
                    if da[2]=="float":
                        rec_data.append(round(app.hex_to_dec(res[da[0]:da[1]])*da[3],1))
                        
        elif isinstance(data, dict):
            rec_data={}
            for key,value in data.items():
                val = value[0].split("-")
                try:
                    if len(value)==1:
                        rec_data[key]=app.hex_to_dec(res[int(val[0]):int(val[1])])
                    elif len(value)==2:
                        if value[1]=="hex":
                            rec_data[key]=res[int(val[0]):int(val[1])]
                    elif len(value)==3:
                        if value[1]=="float":
                            rec_data[key]=round(app.hex_to_dec(res[int(val[0]):int(val[1])])*0.1,1)
                except Exception as e:
                    print e
                    print key
                    print value
        else:
            rec_data="Not of any type"
                                       
        return rec_data
        
            
    
    def data_comparison(self,send_data,rec_data,data_title,logfile,logtofile):
        
        print send_data
        print rec_data
        logtofile(logfile,"字段             send_data       receive_data    \n")
        kk = True
        for j in range(len(send_data)):
            if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                errorinfo="error:\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                logtofile(logfile,data_title[j]+":error   "+str(send_data[j])+"     "+str(rec_data[j])+"\n")
#                     win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                print "error:\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                kk=False
            else:
                if len(data_title[j])<17:
                    if re.findall(r"\w",data_title[j],re.I)!=[]:
                        title = data_title[j].ljust(17-len(data_title[j])+len(re.findall(r"\w",data_title[j],re.I)))
                    else:
                        title = data_title[j].ljust(17-len(data_title[j]))
                else:
                    print data_title[j]
                if len(str(send_data[j]).strip())<17:
                    send = str(send_data[j]).strip().ljust(17-len(str(send_data[j]).strip()))
                else:
                    print str(send_data[j]).strip()
               
                if len(str(rec_data[j]).strip())<17:
                    if data_title[j]=="手机号":
                        rec ="     "+str(rec_data[j]).strip()
                    else:
                        rec = str(rec_data[j]).strip().ljust(17-len(str(rec_data[j]).strip()))  
                else:
                    print  str(rec_data[j]).strip()  
                                       
                logtofile(logfile,title+send+rec+"\n")
                
        if kk==False:
            return False  
        
        return True   
    
    
    
    