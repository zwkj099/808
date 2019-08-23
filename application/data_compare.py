# -*- coding: utf-8 -*-
import application
# import win32api
# import win32con
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class data_compare(object):
    def __init__(self):
        pass
    def poling_compare(self,data1,data2,mobile,logfile,logtofile):
        sensordic = {"21":"21温度传感器","22":"22温度传感器","23":"23温度传感器","24":"24温度传感器","25":"25温度传感器","26":"26湿度传感器","27":"27湿度传感器","28":"28湿度传感器",\
                     "29":"29湿度传感器","2A":"2A湿度传感器","41":"41油量传感器","42":"42油量传感器","43":"43油量传感器","44":"44油量传感器","45":"45油耗传感器","46":"46油耗传感器",\
                     "47":"47液位传感器","48":"48液位传感器","49":"49液位传感器","4A":"4A液位传感器","51":"51正反转","53":"53里程传感器","66":"66胎压传感器4轮","70":"70载重传感器",\
                     "71":"71载重传感器","80":"80工时传感器","81":"81工时","90":"90车载终端IO","91":"91外接IO控制器","92":"92外接IO控制器","E5":"E5原车OBD","E3":"胎压传感器"}
        app = application.application()
        plate_number, sensor, timestr = data1  #桂A00002,21温度传感器,4
        mobile = mobile
        sensorid = ""
        for key,value in sensordic.items():
            if value==sensor:
                sensorid = key
                break
        if sensorid=="":
            win32api.MessageBox(0, "error:config file cann't find the sensorid", "Fail",win32con.MB_ICONWARNING)
            print "error:config file cann't find the sensorid"
        data = data2 #7E 89 00 00 06 01 87 76 76 32 02 04 93 FA 01 21 02 04 06 74 7E
        print "data:"
        print data
        if data[10:11]=="0":
            simcard = data[11:22]
        else:
            simcard = data[10:22]
        transmission_type = data[26:28]
        packages_number = data[28:30]
        peripheral_id = data[30:32]
        data_lenght = data[32:34]
        polling_time = app.hex_to_dec(data[34:36])
        
        send_data =[mobile,'FA','01',sensorid,'02',int(timestr)]
        
        rec_data = [simcard,transmission_type,packages_number,peripheral_id,data_lenght,polling_time]
#         data_title=["simcard","transmission_type","packages_number","peripheral_id","data_lenght","polling_time"]
        logtofile(logfile,"字段             send_data       receive_data    \n")
        data_title=[u"手机号",u"透传消息类型",u"包总数",u"外设ID",u"数据长度",u"轮询时间"]
        kk = True
        for j in range(len(send_data)):
            if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                errorinfo="error:"+sensor+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                logtofile(logfile,data_title[j]+":error "+str(send_data[j])+"     "+str(rec_data[j])+"\n")
#                 win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                print "error:"+sensor+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                kk=False
            else:
                try:
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
                except Exception as e:
                    print e
        if kk==False:
                return False
        
        return True
    
    def load_compare(self,sensor_data,calibration,res,mobile,logfile,logtofile):
        app = application.application()
        
        no,plate_number,sensor,baudrate,filterfactor,compensate,oddEvenCheck,loadMeterWay,loadMeterUnit,noLoadValue,\
            noLoadThreshold,lightLoadValue,lightLoadThreshold,fullLoadValue,fullLoadThreshold,overLoadValue,overLoadThreshold=sensor_data

        peripheral_id =str(no)   
        
        logtofile(logfile,"data comparison as below: ")
        if res[2:6]=="8103":
            
            rec_id =  res[34:36]
            f3_id = res[32:34]
            rec_lenght = res[36:38]
            #补偿使能
            compensate_dic={1:"使能",2:"禁用"}
            rec_compensate=compensate_dic[app.hex_to_dec(res[38:42])]
            #滤波方式 
            filterfactor_dic={1:"实时",2:"平滑",3:"平稳"}
            rec_filterfactor=filterfactor_dic[app.hex_to_dec(res[42:46])]
            #重量单位
#             loadMeterUnit_dic={0:"0.1kg",1:"1kg",2:"10kg",3:"100kg"} 
            rec_loadMeterUnit = app.hex_to_dec(res[74:78])
            #载重测量方案
#             loadMeterWay_dic={0:"状态判断",1:"单计重",2:"双计重",4:"四计重"}
            rec_loadMeterWay= app.hex_to_dec(res[94:98])
            
            rec_overLoadValue = app.hex_to_dec(res[86:90])
            rec_overLoadThreshold = app.hex_to_dec(res[90:94])
            
            rec_fullLoadValue = app.hex_to_dec(res[98:102])
            rec_fullLoadThreshold = app.hex_to_dec(res[102:106])
            
            rec_noLoadValue = app.hex_to_dec(res[106:110])
            rec_noLoadThreshold = app.hex_to_dec(res[110:114])
            
            rec_lightLoadValue = app.hex_to_dec(res[114:118])
            rec_lightLoadThreshold = app.hex_to_dec(res[118:122])
            
            data_lenght=len(res)   #154
            
            rec_data=[f3_id,rec_id,data_lenght,rec_lenght,rec_compensate,rec_filterfactor,rec_loadMeterUnit,rec_loadMeterWay,rec_overLoadValue,\
                      rec_overLoadThreshold,rec_fullLoadValue,rec_fullLoadThreshold,rec_noLoadValue,rec_noLoadThreshold,rec_lightLoadValue,\
                      rec_lightLoadThreshold]  
            send_data=["F3",peripheral_id,154,"38",compensate,filterfactor,loadMeterUnit,loadMeterWay,overLoadValue,overLoadThreshold,fullLoadValue,\
                       fullLoadThreshold,noLoadValue,noLoadThreshold,lightLoadValue,lightLoadThreshold]    
            
#             data_title=["F3","id","data_lenght","lenght","compensate","filterfactor","loadMeterUnit","loadMeterWay","overLoadValue",\
#                       "overLoadThreshold","fullLoadValue","fullLoadThreshold","noLoadValue","noLoadThreshold","lightLoadValue",\
#                       "lightLoadThreshold"]      
            data_title=[u"透传消息类型",u"外设ID",u"消息总长度",u"数据长度",u"补偿使能",u"滤波方式",u"重量单位",u"载重测量方案",u"超载阈值",\
                      u"超载阈值偏差",u"满载阈值",u"满载阈值偏差",u"空载阈值",u"空载阈值偏差",u"轻载阈值",\
                      u"轻载阈值偏差"]        
            logtofile(logfile,"字段             send_data       receive_data    \n")  
            kk = True
            for j in range(len(send_data)):
                if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                    errorinfo="error:"+sensor+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    logtofile(logfile,data_title[j]+":error   "+str(send_data[j])+"     "+str(rec_data[j])+"\n")
#                     win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                    print "error:"+sensor+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
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
            
        elif res[2:6]=="8900":
            kj=True
            rec_id = res[30:32]
            f_id = res[26:28]
            data_count = res[28:30]
            group_number=res[32:34]
            f_ad = app.hex_to_dec(res[34:42])
            f_weight = float(app.hex_to_dec(res[42:50]))
            s_ad = app.hex_to_dec(res[50:58])
            s_weight = float(app.hex_to_dec(res[58:66]))
            t_ad = app.hex_to_dec(res[66:74])
            t_weight = float(app.hex_to_dec(res[74:82]))
            
            data_lenght = len(res)#102
            
            #只验证标定组数为3的数据，不然报错
            rec_data=[f_id,rec_id,data_lenght,data_count,group_number,f_ad,f_weight,s_ad,s_weight,t_ad,t_weight]
            
            send_data=["F6",peripheral_id,102,"01","04",calibration[0][0],calibration[0][1],calibration[1][0],calibration[1][1],\
                       calibration[2][0],calibration[2][1]]
#             data_title=["f_id","id","data_lenght","data_count","group_number","f_ad","f_weight","s_ad","s_weight","t_ad","t_weight"]
            logtofile(logfile,"字段             send_data       receive_data    \n")
            data_title=[u"透传消息类型",u"外设ID",u"消息总长度",u"消息包总数",u"标定组数",u"AD值",u"车辆载荷重量",u"AD值",u"车辆载荷重量",u"AD值",u"车辆载荷重量"]
            for j in range(len(send_data)):
                if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                    logtofile(logfile,data_title[j]+":error    "+str(send_data[j])+"      "+str(rec_data[j])+"\n")
                    errorinfo="error:"+sensor+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    
#                     win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                    print "error:"+sensor+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    kj = False
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
            if kj==False:
                return False
        else:
            return False
        
                   
        return True
    
    
    
    def oil_compare(self,sensor_data,calibration,res,mobile,logfile,logtofile):
        app = application.application()
        plate_number,no,oil_type,shape1Hidden,box_length,box_width,box_height,box_tick,theory_volume,actual_volume,\
                         sensor_type,sensor_length,baudrate,filterfactor,compensate,oddEvenCheck,group_num1,autouploadtime1,output_k1,\
                         output_b1,addoiltime1,addoil1,seepoiltime1,seepoil1=sensor_data
        if res[2:6]=="8103":
            print "compare:"+res
            data_lenght = len(res)#154
            packet_num = res[26:28]
            f3_id = res[32:34]
            rec_id =res[34:36]
            rec_lenght = res[36:38]            #补偿使能
            compensate_dic={1:"使能",2:"禁用"}
            rec_compensate=app.hex_to_dec(res[38:42])
            #滤波方式 
            filterfactor_dic={1:"实时",2:"平滑",3:"平稳"}
            rec_filterfactor=app.hex_to_dec(res[42:46])
            rec_autouploadtime=app.hex_to_dec(res[46:50])
            rec_outputk = app.hex_to_dec(res[50:54])
            rec_outputb = app.hex_to_dec(res[54:58])
            rec_sensor_length = int(app.hex_to_dec(res[82:86])*0.1)
            rec_fuel_select = app.hex_to_dec(res[90:94])#1
            rec_shape = app.hex_to_dec(res[94:98])
            rec_box_lenght = app.hex_to_dec(res[98:102])
            rec_box_width = app.hex_to_dec(res[102:106])
            rec_box_height = app.hex_to_dec(res[106:110])
            rec_addoiltime = app.hex_to_dec(res[114:118])
            rec_addoil = int(app.hex_to_dec(res[118:122])*0.1)
            rec_seepoiltime = app.hex_to_dec(res[122:126])
            rec_seepoil = int(app.hex_to_dec(res[126:130])*0.1)
            
            rec_data = [data_lenght,packet_num,f3_id,rec_id,rec_lenght,rec_compensate,rec_filterfactor,rec_autouploadtime,rec_outputk,rec_outputb,\
                        rec_sensor_length,rec_fuel_select,rec_shape,rec_box_lenght,rec_box_width,rec_box_height,rec_addoiltime,rec_addoil,\
                        rec_seepoiltime,rec_seepoil]
            send_data = [154,"01","F3",no,"38",int(compensate),int(filterfactor),int(autouploadtime1),output_k1,output_b1,sensor_length,"1",shape1Hidden,\
                         box_length,box_width,box_height,addoiltime1,addoil1,seepoiltime1,seepoil1]
            
            
#             data_title=["data_lenght","packet_num","f3_id","rec_id","rec_lenght","rec_compensate","rec_filterfactor","rec_autouploadtime","rec_outputk","rec_outputb",\
#                         "rec_sensor_length","rec_fuel_select","rec_shape","rec_box_lenght","rec_box_width","rec_box_height","rec_addoiltime","rec_addoil",\
#                         "rec_seepoiltime","rec_seepoil"]
            data_title=[u"消息总长度",u"消息包总数",u"透传消息类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"自动上传时间",u"输出修正系数 K",u"输出修正常数 B",\
                        u"传感器长度",u"燃料选择",u"容器形状",u"容器尺寸 1",u"容器尺寸 2",u"容器尺寸 3",u"加液时间阈值",u"加液量阈值",\
                        u"漏液时间阈值",u"漏液量阈值"]
            logtofile(logfile,"字段             send_data       receive_data    \n")
            kk = True
            for j in range(len(send_data)):
                if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                    errorinfo="error:"+oil_type+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    logtofile(logfile,data_title[j]+":error    "+str(send_data[j])+"      "+str(rec_data[j])+"\n")
#                     win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                    print "error:"+oil_type+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    KK=False
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

        elif res[2:6]=="8900":
            kj=True
            rec_id = res[30:32]
            f_id = res[26:28]
            data_count = res[28:30]
            group_number=app.hex_to_dec(res[32:34])
            rec_calibration = {}
            j = 34
            for i in range(int(group_num1)):
                rec_calibration[i]=(round(app.hex_to_dec(res[j:j+8])*0.1,1),round((app.hex_to_dec(res[j+8:j+16]))*0.1,1))
                j = j + 16

            #只验证标定组数为3的数据，不然报错
            rec_data=[f_id,rec_id,data_count,group_number]
            
            send_data=["F6",rec_id,"01",int(group_num1)+1]
            
#             data_title=["f_id","rec_id","data_count","group_number"]
            logtofile(logfile,"字段             send_data       receive_data    \n")
            data_title=[u"透传消息类型",u"外设ID",u"数据总数",u"标定组数"]
            for j in range(len(send_data)):
                if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                    errorinfo="error:"+oil_type+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    logtofile(logfile,data_title[j]+":error    "+str(send_data[j])+"      "+str(rec_data[j])+"\n")
#                     win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                    print "error:"+oil_type+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    KK=False
                else:
                    if len(data_title[j])<17:
                        if re.findall(r"\w",data_title[j],re.I)!=[]:
                            title = data_title[j].ljust(17-len(data_title[j])+len(re.findall(r"\w",data_title[j],re.I)))
                        else:
                            title = data_title[j].ljust(17-len(data_title[j]))
                    else:

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
            logtofile(logfile,u"标定数据:")        
            for k in range(int(group_num1)):
                if round(float(calibration[k][0]),1)!=round(float(rec_calibration[k][0]),1) or round(float(calibration[k][1]),1)!=round(float(rec_calibration[k][1]),1) :
                    kj = False
                    print str(calibration[k]) + " with "+str(rec_calibration[k])+" not match"
                    logtofile(logfile,"error:    "+str(calibration[k])+"       "+str(rec_calibration[k])+"\n")
                    errorinfo = str(calibration[k]) + " with "+str(rec_calibration[k])+" not match"
                    #win32api.MessageBox(0, errorinfo, errorinfo,win32con.MB_ICONWARNING)
                else:
                    
                    logtofile(logfile,"     "+str(calibration[k])+"     "+str(rec_calibration[k])+"\n")
            
            if kj==False:
                return False
            
            
        return True
    
    def oilwear_compare(self,sensor_data,res,mobile,logfile,logtofile):
        app = application.application()
        plate_number,sensor_type,baudrate,filterfactor,compensate,oddEvenCheck,autouploadtime1,output_k1,output_b1=sensor_data
        if res[2:6]=="8103":
            
            #7E810300240187767632020730010000F3451E0001000200010064006400000000000000000000000000000000000200018F7E
            try:
                data_lenght = len(res)#102
                packet_num = res[26:28]
                f3_id = res[32:34]
                rec_id =res[34:36]
                rec_lenght = res[36:38]            #补偿使能
                compensate_dic={1:"使能",2:"禁用"}
                rec_compensate=app.hex_to_dec(res[38:42])
                #滤波方式 
                filterfactor_dic={1:"实时",2:"平滑",3:"平稳"}
                rec_filterfactor=app.hex_to_dec(res[42:46])
                rec_autouploadtime=app.hex_to_dec(res[46:50])
                rec_outputk = app.hex_to_dec(res[50:54])
                rec_outputb = app.hex_to_dec(res[54:58])
                rec_holditem1 = app.hex_to_dec(res[58:98])
                rec_oiltype = app.hex_to_dec(res[98:102])
                rec_measuretype = app.hex_to_dec(res[102:106])
                rec_holditem2 = app.hex_to_dec(res[106:150])
            except Exception as e:
                print e
                print "oil wear rec data error"
                return False

            
            rec_data = [data_lenght,packet_num,f3_id,rec_id,rec_lenght,rec_compensate,rec_filterfactor,rec_autouploadtime,rec_outputk,rec_outputb]
            send_data = [154,"01","F3","45","38",int(compensate),int(filterfactor),int(autouploadtime1),output_k1,output_b1]
            
            
#             data_title=["data_lenght","packet_num","f3_id","rec_id","rec_lenght","rec_compensate","rec_filterfactor","rec_autouploadtime","rec_outputk","rec_outputb"]
            data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"自动上传时间",u"输出修正系数 K",u"输出修正常数 B"]
            logtofile(logfile,"字段             send_data       receive_data    \n")
            kk = True
            for j in range(len(send_data)):
                if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                    errorinfo="error:oil wear\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    logtofile(logfile,data_title[j]+":error:     "+str(send_data[j])+"      "+str(rec_data[j])+"\n")
#                     win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                    print "error:oil wear\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    KK=False
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

        elif res[2:6]=="8900":
            print "oil wear no 8900"
            return False

            
        return True
    
    
    def mileage_compare(self,sensor_data,res,mobile,logfile,logtofile):
        app = application.application()
        plate_number,measurementScheme,sensor_type,baudrate,filterfactor,compensate,oddEvenCheck,autouploadtime1,output_k1,output_b1,\
                 tyreSizeId,tyreRollingRadius,rollingRadius=sensor_data
        
        if res[2:6]=="8103":
            
            #7E8103003E0187767632020735010000F35338000100000002006300630000000000000000000000000200BB8003E800020000000000000000000000000000000000000000000000000000727E
            try:
                data_lenght = len(res)#154
                packet_num = res[26:28]
                f3_id = res[32:34]
                rec_id =res[34:36]
                rec_lenght = res[36:38]            #补偿使能
                compensate_dic={1:"使能",2:"禁用"}
                rec_compensate= compensate_dic[app.hex_to_dec(res[38:42])]
                rec_holditem0 = app.hex_to_dec(res[42:46])
                rec_autouploadtime=app.hex_to_dec(res[46:50])
                rec_outputk = app.hex_to_dec(res[50:54])
                rec_outputb = app.hex_to_dec(res[54:58])
                rec_holditem1 = app.hex_to_dec(res[58:82])
                rec_tyreRollingRadius = app.hex_to_dec(res[82:86])
                rec_rollingRadius = app.hex_to_dec(res[86:90])
                rec_velocityratio = app.hex_to_dec(res[90:94])#轮速，默认没有
                rec_measurementScheme = app.hex_to_dec(res[94:98])#默认选02
                rec_measurebasevalue = app.hex_to_dec(res[98:106])
                rec_holditem2 = app.hex_to_dec(res[106:150])
            except Exception as e:
                print e
                print "mileage rec data error"
                return False

            if rec_measurementScheme!=1:#不是原车脉冲
                rec_data = [data_lenght,packet_num,f3_id,rec_id,rec_lenght,rec_compensate,rec_autouploadtime,rec_outputk,rec_outputb, rec_tyreRollingRadius,\
                            rec_rollingRadius,rec_measurementScheme]
                send_data = [154,"01","F3","53","38",compensate,autouploadtime1,output_k1,output_b1,tyreRollingRadius,rollingRadius,rec_measurementScheme]
                print rec_data
                print send_data
                
                data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"自动上传时间",u"输出修正系数 K",u"输出修正常数 B",\
                            u"轮胎滚动半径",u"滚动半径修正系数",u"里程测量方案"]
#                 data_title=["data_lenght","packet_num","f3_id","rec_id","rec_lenght","rec_compensate","rec_autouploadtime","rec_outputk","rec_outputb",\
#                             "rec_tyreRollingRadius","rec_rollingRadius","rec_measurementScheme"]
                logtofile(logfile,"字段             send_data       receive_data    \n")
                kk = True
                for j in range(len(send_data)):
                    if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                        logtofile(logfile,data_title[j]+":error:     "+str(send_data[j])+"      "+str(rec_data[j])+"\n")
                        errorinfo="error:Mileage"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                        
#                         win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                        print "error:Mileage"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
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
    
            elif res[2:6]=="8900":
                print "mileage no 8900"
                return False
            else:
                return False

            
        return True
        
        
        
    def temp_compare(self,sensor_data,res,mobile,logfile,logtofile):
        app = application.application()
        plate_number,sensor_type,filterfactor,compensate,autouploadtime,overValve,output_k,output_b,\
                         alarmUp,alarmDown=sensor_data
        
        if res[2:6]=="8103":  
            #E8103003E018776763202073E010000F321380001000200010065006500000000000000000000000000000B0F0AB500230000000000000000000000000000000000000000000000000000427E
            try:
                data_lenght = len(res)#154
                packet_num = res[26:28]
                f3_id = res[32:34]
                rec_id =res[34:36]
                rec_lenght = res[36:38]            #补偿使能
                compensate_dic={1:"使能",2:"禁用"}
                rec_compensate= app.hex_to_dec(res[38:42])
                rec_filterfactor = app.hex_to_dec(res[42:46])
                rec_autouploadtime=app.hex_to_dec(res[46:50])
                rec_outputk = app.hex_to_dec(res[50:54])
                rec_outputb = app.hex_to_dec(res[54:58])
                rec_holditem1 = app.hex_to_dec(res[58:86])
                rec_alarmUp = int(app.hex_to_dec(res[86:90])*0.1-273.1)
                rec_alarmDown = int(app.hex_to_dec(res[90:94])*0.1-273.1)
                rec_overValve = app.hex_to_dec(res[94:98])#默认选02
                rec_holditem2 = app.hex_to_dec(res[98:150])
            except Exception as e:
                print e
                print "temp rec data error"
                return False

            rec_data = [data_lenght,packet_num,f3_id,rec_id,rec_lenght,rec_compensate,rec_filterfactor,rec_autouploadtime,rec_outputk,\
                        rec_outputb,rec_alarmUp,rec_alarmDown,rec_overValve]
            send_data = [154,"01","F3","21","38",compensate,filterfactor,autouploadtime,output_k,output_b,alarmUp,alarmDown,overValve]
            print rec_data
            print send_data
            
            logtofile(logfile,"字段             send_data       receive_data    \n")
            data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"自动上传时间",u"输出修正系数 K",u"输出修正常数 B",\
                        u"温度报警上阈值",u"温度报警下阈值",u"超出阈值时间阈值"]
#             data_title=["data_lenght","packet_num","f3_id","rec_id","rec_lenght","rec_compensate","rec_filterfactor","rec_autouploadtime","rec_outputk","rec_outputb",\
#                         "rec_alarmUp","rec_alarmDown","rec_overValve"]
            kk = True
            for j in range(len(send_data)):
                if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                    logtofile(logfile,data_title[j]+":error:     "+str(send_data[j])+"      "+str(rec_data[j])+"\n")
                    errorinfo="error:Temp"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    
                    #win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                    print "error:Temp"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
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

        elif res[2:6]=="8900":
            print "temp no 8900"
            return False


        return True
    
    def wetness_compare(self,sensor_data,res,mobile,logfile,logtofile):
        app = application.application()
        plate_number,sensor_type,filterfactor,compensate,autouploadtime,overValve,output_k,output_b,\
                         alarmUp,alarmDown=sensor_data
        
        if res[2:6]=="8103":  
            #E8103003E018776763202073E010000F321380001000200010065006500000000000000000000000000000B0F0AB500230000000000000000000000000000000000000000000000000000427E
            try:
                data_lenght = len(res)#154
                packet_num = res[26:28]
                f3_id = res[32:34]
                rec_id =res[34:36]
                rec_lenght = res[36:38]            #补偿使能
                compensate_dic={1:"使能",2:"禁用"}
                rec_compensate= app.hex_to_dec(res[38:42])
                filterfactor_dic={1:"实时",2:"平滑",3:"平稳"}
                rec_filterfactor =app.hex_to_dec(res[42:46])
                rec_autouploadtime=app.hex_to_dec(res[46:50])
                rec_outputk = app.hex_to_dec(res[50:54])
                rec_outputb = app.hex_to_dec(res[54:58])
                rec_holditem1 = app.hex_to_dec(res[58:86])
                rec_alarmUp = int(app.hex_to_dec(res[86:90])*0.1)
                rec_alarmDown = int(app.hex_to_dec(res[90:94])*0.1)
                rec_overValve = app.hex_to_dec(res[94:98])#默认选02
                rec_holditem2 = app.hex_to_dec(res[98:150])
            except Exception as e:
                print e
                print "wetness rec data error"
                return False

            rec_data = [data_lenght,packet_num,f3_id,rec_id,rec_lenght,rec_compensate,rec_filterfactor,rec_autouploadtime,rec_outputk,\
                        rec_outputb,rec_alarmUp,rec_alarmDown,rec_overValve]
            send_data = [154,"01","F3","26","38",compensate,filterfactor,autouploadtime,output_k,output_b,alarmUp,alarmDown,overValve]
            print rec_data
            print send_data
            logtofile(logfile,"字段             send_data       receive_data    \n")
            data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"自动上传时间",u"输出修正系数 K",u"输出修正常数 B",\
                        u"湿度报警上阈值",u"湿度报警下阈值",u"超出阈值时间阈值"]
            
#             data_title=["data_lenght","packet_num","f3_id","rec_id","rec_lenght","rec_compensate","rec_filterfactor","rec_autouploadtime","rec_outputk","rec_outputb",\
#                         "rec_alarmUp","rec_alarmDown","rec_overValve"]
            kk = True
            for j in range(len(send_data)):
                if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                    logtofile(logfile,data_title[j]+":error:     "+str(send_data[j])+"     "+str(rec_data[j])+"\n")
                    errorinfo="error:wetness"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    
#                     win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                    print "error:wetness"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
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

        elif res[2:6]=="8900":
            print "wetness no 8900"
            return False


        return True
    
    def reversible_compare(self,sensor_data,res,mobile,logfile,logtofile):
        app = application.application()
        plate_number,sensor_type,compensate,autouploadtime,output_k,output_b=sensor_data
        
        if res[2:6]=="8103":  
            #E8103003E018776763202073E010000F321380001000200010065006500000000000000000000000000000B0F0AB500230000000000000000000000000000000000000000000000000000427E
            try:
                data_lenght = len(res)#154
                packet_num = res[26:28]
                f3_id = res[32:34]
                rec_id =res[34:36]
                rec_lenght = res[36:38]            #补偿使能
                compensate_dic={1:"使能",2:"禁用"}
                rec_compensate= app.hex_to_dec(res[38:42])
                rec_holditem0 = app.hex_to_dec(res[42:46])
                rec_autouploadtime=app.hex_to_dec(res[46:50])
                rec_outputk = app.hex_to_dec(res[50:54])
                rec_outputb = app.hex_to_dec(res[54:58])
                rec_holditem1 = app.hex_to_dec(res[58:150])

            except Exception as e:
                print e
                print "reversible rec data error"
                return False

            rec_data = [data_lenght,packet_num,f3_id,rec_id,rec_lenght,rec_compensate,rec_autouploadtime,rec_outputk,rec_outputb]
            send_data = [154,"01","F3","51","38",compensate,autouploadtime,output_k,output_b]
            print rec_data
            print send_data
            logtofile(logfile,"字段             send_data       receive_data    \n")
            data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"补偿使能",u"自动上传时间",u"输出修正系数 K",u"输出修正常数 B"]
#             data_title=["data_lenght","packet_num","f3_id","rec_id","rec_lenght","rec_compensate","rec_autouploadtime","rec_outputk","rec_outputb"]
            kk = True
            for j in range(len(send_data)):
                if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                    logtofile(logfile,data_title[j]+":error     "+str(send_data[j])+"     "+str(rec_data[j])+"\n")
                    errorinfo="error:Reversible"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    
#                     win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                    print "error:Reversible"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
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

        elif res[2:6]=="8900":
            print "reversible no 8900"
            return False


        return True   
  
    def obd_compare(self,sensor_data,res,mobile,logfile,logtofile):
        app = application.application()
        plate_number,device_type,typeList,vehicleTypeId,autouploadtime=sensor_data
        
        if res[2:6]=="8103":  
            
            try:
                data_lenght = len(res)#58
                packet_num = res[26:28]
                f3_id = res[32:34]
                rec_id =res[34:36]
                rec_lenght = res[36:38]         
                rec_vehicleTypeId= app.hex_to_dec(res[38:46])
                rec_autouploadtime=int(app.hex_to_dec(res[46:54])*0.001)

            except Exception as e:
                print e
                print "OBD rec data error"
                return False

            rec_data = [data_lenght,packet_num,f3_id,rec_id,rec_lenght, rec_vehicleTypeId,rec_autouploadtime]
            send_data = [58,"01","F3","E5","08",app.hex_to_dec(vehicleTypeId),autouploadtime]
            print rec_data
            print send_data
            logtofile(logfile,"字段             send_data       receive_data    \n")
            data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"车型ID",u"数据流上传时间间隔"]
#             data_title=["data_lenght","packet_num","f3_id","rec_id","rec_lenght","rec_vehicleTypeId","rec_autouploadtime"]
            kk = True
            for j in range(len(send_data)):
                if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                    logtofile(logfile,data_title[j]+":error    "+str(send_data[j])+"      "+str(rec_data[j])+"\n")
                    errorinfo="error:OBD"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    
#                     win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                    print "error:OBD"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
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

        elif res[2:6]=="8900":
            print "OBD no 8900"
            return False


        return True   
    
    def psi_compare(self,sensor_data,res,mobile,logfile,logtofile):
        app = application.application()
        plate_number,tires_number,sensor_type,filterfactor,compensate,autouploadtime,output_k,output_b,\
                         normalTirePressure,pressureImbalanceThreshold,slowLeakThreshold,highTemperatureThreshold,\
                         lowVoltageThreshold,highVoltageThreshold,powerAlarmThreshold=sensor_data
        
        if res[2:6]=="8103":  
            
            try:
                data_lenght = len(res)#154
                packet_num = res[26:28]
                f3_id = res[32:34]
                rec_id =res[34:36]
                rec_lenght = res[36:38]         
                compensate_dic={1:"使能",2:"禁用"}
                rec_compensate= app.hex_to_dec(res[38:42])
                rec_filterfactor = app.hex_to_dec(res[42:46])
                rec_autouploadtime=app.hex_to_dec(res[46:50])
                rec_outputk = app.hex_to_dec(res[50:54])
                rec_outputb = app.hex_to_dec(res[54:58])
                rec_holditem1 = app.hex_to_dec(res[58:80])
                rec_tirenumb = app.hex_to_dec(res[80:82])#不进行对比，因为界面没有下发此参数
                rec_normalTirePressure = round(app.hex_to_dec(res[82:86])*0.1,1)
                rec_pressureImbalanceThreshold = app.hex_to_dec(res[86:90])
                rec_slowLeakThreshold = app.hex_to_dec(res[90:94])
                rec_lowVoltageThreshold = round(app.hex_to_dec(res[94:98])*0.1,1)
                rec_highVoltageThreshold = round(app.hex_to_dec(res[98:102])*0.1,1)
                rec_highTemperatureThreshold = int(app.hex_to_dec(res[102:106])*0.1-273.1)
                rec_powerAlarmThreshold = app.hex_to_dec(res[106:110])
                rec_holditem2 = app.hex_to_dec(res[110:150])
                

            except Exception as e:
                print e
                print "PSI rec data error"
                return False

            rec_data = [data_lenght,packet_num,f3_id,rec_id,rec_lenght, rec_compensate,rec_filterfactor,rec_autouploadtime,\
                        rec_outputk,rec_outputb,rec_normalTirePressure,rec_pressureImbalanceThreshold,\
                        rec_slowLeakThreshold,rec_lowVoltageThreshold,rec_highVoltageThreshold,rec_highTemperatureThreshold,\
                        rec_powerAlarmThreshold]
            send_data = [154,"01","F3","E3","38",compensate,filterfactor,autouploadtime,output_k,output_b,\
                          normalTirePressure,pressureImbalanceThreshold,slowLeakThreshold,lowVoltageThreshold,highVoltageThreshold,\
                          highTemperatureThreshold,powerAlarmThreshold]
            print rec_data
            print send_data
            logtofile(logfile,"字段             send_data       receive_data    \n")
            data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"自动上传时间",u"输出修正系数 K",u"输出修正常数 B",\
                        u"正常胎压值",u"胎压不平衡门限",u"慢漏气门限",u"低压阈值",u"高压阈值",u"高温阈值",u"传感器电量报警阈值"]
#             data_title=["data_lenght","packet_num","f3_id","rec_id","rec_lenght","rec_compensate","rec_filterfactor","rec_autouploadtime",
#                         "rec_outputk","rec_outputb","rec_normalTirePressure","rec_pressureImbalanceThreshold",\
#                         "rec_slowLeakThreshold","rec_lowVoltageThreshold","rec_highVoltageThreshold","rec_highTemperatureThreshold",\
#                         "rec_powerAlarmThreshold"]
            kk = True
            title=""
            send=""
            rec=""
            for j in range(len(send_data)):
                if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                    errorinfo="error:PSI\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    logtofile(logfile,data_title[j]+":error    "+str(send_data[j])+"      "+str(rec_data[j])+"\n")
#                     win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                    print "error:PSI\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
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

        elif res[2:6]=="8900":
            print "PSI no 8900"
            return False


        return True 
    
    def labor_compare(self,sensor_data,res,mobile,logfile,logtofile):
        app = application.application()

        if res[2:6]=="8103":  
            try:
                data_lenght = len(res)#154
                packet_num = res[26:28]
                f3_id = res[32:34]
                rec_id =res[34:36]
                rec_lenght = res[36:38]            #补偿使能
                compensate_dic={1:"使能",2:"禁用"}
                rec_compensate=compensate_dic[app.hex_to_dec(res[38:42])]
                filterfactor_dic={1:"实时",2:"平滑",3:"平稳"}
                rec_filterfactor = filterfactor_dic[app.hex_to_dec(res[42:46])]
                rec_autouploadtime=app.hex_to_dec(res[46:50])
                rec_outputk = app.hex_to_dec(res[50:54])
                rec_outputb = app.hex_to_dec(res[54:58])
                rec_holditem1 = app.hex_to_dec(res[58:82])
                detectionmode_dic={0:"电压比较式",1:"油耗阈值式",2:"油耗波动式"}
                rec_detectionMode =detectionmode_dic[app.hex_to_dec(res[82:86])]
                rec_thresholdVoltage = round(app.hex_to_dec(res[86:90])*0.1,1)
                rec_Wavecalculatio_number = app.hex_to_dec(res[90:92])
                rec_Wavecalculatio_time = app.hex_to_dec(res[92:94])
                rec_smoothingFactor = app.hex_to_dec(res[94:96])
                rec_lasttimethreshold = app.hex_to_dec(res[96:98])
                rec_holditem2 = app.hex_to_dec(res[98:150])
                
            except Exception as e:
                print e
                print "Labor rec data error"
                return False
            if len(sensor_data)==8:#油耗阈值式
                rec_data=[data_lenght,packet_num,f3_id,rec_id,rec_lenght,rec_compensate,rec_filterfactor,rec_detectionMode,rec_lasttimethreshold]
                data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"工时检测方式",u"状态变换持续时长"]
#                 data_title=["data_lenght","packet_num","f3_id","rec_id","rec_lenght","rec_compensate","rec_filterfactor","rec_detectionMode","rec_lasttimethreshold"]
                send_data=[154,"01","F3","80","38",sensor_data[3],sensor_data[2],sensor_data[4],sensor_data[7]]
            elif len(sensor_data)==9:#电压比较式 
                rec_data=[data_lenght,packet_num,f3_id,rec_id,rec_lenght,rec_compensate,rec_filterfactor,rec_detectionMode,rec_lasttimethreshold,rec_thresholdVoltage]
                send_data=[154,"01","F3","80","38",sensor_data[3],sensor_data[2],sensor_data[4],sensor_data[7],sensor_data[-1]]
                data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"工时检测方式",u"状态变换持续时长",u"阈值,即电压值"]
#                 data_title=["data_lenght","packet_num","f3_id","rec_id","rec_lenght","rec_compensate","rec_filterfactor","rec_detectionMode","rec_lasttimethreshold","rec_thresholdVoltage"]
            else:#油耗波动 
                
                rec_data=[data_lenght,packet_num,f3_id,rec_id,rec_lenght,rec_filterfactor,rec_compensate,rec_detectionMode,rec_lasttimethreshold,\
                          rec_Wavecalculatio_number,rec_smoothingFactor,rec_Wavecalculatio_time]
                send_data=[154,"01","F3","80","38"]
                logtofile(logfile,"字段             send_data       receive_data    \n")
                data_title=[u"数据总长度",u"数据包总数",u"数据透传类型",u"外设ID",u"数据长度",u"补偿使能",u"滤波方式",u"工时检测方式",u"状态变换持续时长",\
                            u"波动计算个数",u"平滑参数",u"波动计算时间段"]
#                 data_title=["data_lenght","packet_num","f3_id","rec_id","rec_lenght","rec_filterfactor","rec_compensate","rec_detectionMode","rec_lasttimethreshold",\
#                           "rec_Wavecalculatio_number","rec_smoothingFactor","rec_Wavecalculatio_time"]
                for i in sensor_data:
                    if sensor_data.index(i) not in [0,1,5,6,10,12]:#界面上的奇偶校验、波特率、波动阈值、速度阈值在协议中没有，无法比较
                        send_data.append(i)

            print rec_data
            print send_data

            

            kk = True
            for j in range(len(send_data)):
                if str(send_data[j]).strip()!= str(rec_data[j]).strip():
                    logtofile(logfile,data_title[j]+":error   "+str(send_data[j])+"     "+str(rec_data[j])+"\n")
                    errorinfo="error:Labor"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
                    
                    #win32api.MessageBox(0, errorinfo, "Fail",win32con.MB_ICONWARNING)
                    print "error:Labor"+"\n"+data_title[j]+" \nsend data: "+str(send_data[j])+" with receive data: "+str(rec_data[j])+ " not match"
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

        elif res[2:6]=="8900":
            print "Labor no 8900"
            return False


        return True
  
    
    
    
    