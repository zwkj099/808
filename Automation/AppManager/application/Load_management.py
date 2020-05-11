# -*- coding: utf-8 -*-
import time
# from splinter import Browser
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

from selenium.webdriver.support.select import Select
import TAException
reload(sys)
sys.setdefaultencoding('utf8')
class load_management(object):
    def __init__(self):
        pass
        #self.browser = webdriver.Firefox()
    def set_load_parameter(self,loaddata,browser,count,vnum,logfile,logtofile):
        self.browser = browser
        if count==0:
#         # 应用管理id
#             time.sleep(5)
#             self.browser.find_element_by_id('9f5ea704-6a90-11e6-8b77-86f30ca893d3').click()
            # 载重管理id
            time.sleep(3)
            self.browser.find_element_by_id('0c60fc30-71d9-4dc2-a773-eb568a5f9ba4').click()
            logtofile(logfile,"click the load management id success\n")
            # 载重管理设置id
            time.sleep(3)
            self.browser.find_element_by_id('0c60fc30-71d9-4dc2-a773-eb568a5f9ba6').click()
            logtofile(logfile,"click the load management settings id success\n")
            time.sleep(5)
            # 搜索框输入桂A00002
            self.browser.find_element_by_id('simpleQueryParam').send_keys(vnum)
            logtofile(logfile,"input sim card into search box:"+vnum+"\n")
            time.sleep(5)
            # 点击搜索按钮
            self.browser.find_element_by_id('search_button').click()
            logtofile(logfile,"click the search button\n")
            
        noLoadValue,noLoadThreshold,lightLoadValue,lightLoadThreshold,fullLoadValue,fullLoadThreshold,overLoadValue,overLoadThreshold=loaddata
        time.sleep(3)
        # 点击第一个按钮设置、修改

        buttontext = self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2]. \
             find_elements_by_tag_name('button')[0].text
        
        logtofile(logfile,"get setting/modify button's text:"+buttontext+"\n")
        
        self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[0].click()
        logtofile(logfile,"click the setting/modify button success\n")
        
        if buttontext==("修改1").decode("utf-8"):
            
            time.sleep(10)
            plate_number =self.browser.find_element_by_id("brands").get_attribute('value')
            time.sleep(3)
            sensor = self.browser.find_element_by_id("sensorType").get_attribute('value')
            time.sleep(3)
            timestr = self.browser.find_element_by_id("pollingTime_3").get_attribute('value')
            # 点关闭按钮
            self.browser.find_element_by_id('doCloseEdit').click()
        else:
            print "设置"
            time.sleep(8)
            logtofile(logfile,"set the load parameters\n")
            # 点击传感器下拉框
            self.browser.find_element_by_id("bindForm").find_elements_by_tag_name('div')[0].find_elements_by_tag_name('div')[0].find_elements_by_tag_name('div')[0].\
               find_elements_by_tag_name('div')[0].find_elements_by_tag_name('button')[0].click()
            
            time.sleep(3)
            no=0
            if self.browser.find_element_by_id("egine1Title").get_attribute("class")=="active":
                no = 70
            else:
                no = 71
            time.sleep(3)
            # 选择传感器类型
            self.browser.find_elements_by_class_name("bssuggest-row")[0].click()
            
            time.sleep(3)
            # 展开隐藏参数
            self.browser.find_element_by_id("tankBasisInfo").click()
            time.sleep(3)
            plate_number =self.browser.find_element_by_id("brands").get_attribute('value')
            
            
            time.sleep(3)
            try:
                sensor = self.browser.find_element_by_id("sensorId").get_attribute('value')
            except Exception as e:
                print e
                sensor = self.browser.find_element_by_id("sensorId1").get_attribute('value')
                
            baudrate = self.browser.find_element_by_name("baudRate").get_attribute('value')
            filterfactor = self.browser.find_element_by_name("filterFactor").get_attribute('value')
            compensate = self.browser.find_element_by_name("compensate").get_attribute('value')
            oddEvenCheck = self.browser.find_element_by_name("oddEvenCheck").get_attribute('value')           
            
            #选择计重方式,选择第一项
            s = Select(self.browser.find_element_by_id("loadMeterWay"))
            s.select_by_index(0)
            time.sleep(5)
            loadMeterWay = self.browser.find_element_by_id("loadMeterWay").get_attribute('value') 
            loadMeterWay = int(loadMeterWay)+1
                          
            #选择传感器重量单位
            s = Select(self.browser.find_element_by_id("loadMeterUnit"))
            s.select_by_index(1) 
            time.sleep(5) 
            loadMeterUnit = self.browser.find_element_by_id("loadMeterUnit").get_attribute('value') 
                    
                     
            loadlist=[noLoadValue,noLoadThreshold,lightLoadValue,lightLoadThreshold,fullLoadValue,fullLoadThreshold,overLoadValue,overLoadThreshold]    
            loadid=["noLoadValue","noLoadThreshold","lightLoadValue","lightLoadThreshold","fullLoadValue","fullLoadThreshold","overLoadValue","overLoadThreshold"]
#             print "loadlist:"
#             print loadlist
            time.sleep(3)
            for i in range(len(loadlist)):
                self.browser.find_element_by_id(loadid[i]).clear()
                # 输入轮询时间
                self.browser.find_element_by_id(loadid[i]).send_keys(loadlist[i])
                time.sleep(3)
   
            noLoadValue1 =self.browser.find_element_by_id("noLoadValue").get_attribute('value')
            noLoadThreshold1 = self.browser.find_element_by_id("noLoadThreshold").get_attribute('value')
            lightLoadValue1 = self.browser.find_element_by_id("lightLoadValue").get_attribute('value')
            lightLoadThreshold1 = self.browser.find_element_by_id("lightLoadThreshold").get_attribute('value')
            fullLoadValue1 =self.browser.find_element_by_id("fullLoadValue").get_attribute('value')
            fullLoadThreshold1 = self.browser.find_element_by_id("fullLoadThreshold").get_attribute('value')
            overLoadValue1 = self.browser.find_element_by_id("overLoadValue").get_attribute('value')
            overLoadThreshold1 = self.browser.find_element_by_id("overLoadThreshold").get_attribute('value')
           
           
            sensor_data=[no,plate_number,sensor,baudrate,filterfactor,compensate,oddEvenCheck,loadMeterWay,loadMeterUnit,noLoadValue1,\
                         noLoadThreshold1,lightLoadValue1,lightLoadThreshold1,fullLoadValue1,fullLoadThreshold1,overLoadValue1,overLoadThreshold1]
            
#             print sensor_data
            #设置标定数据
            time.sleep(5)
            self.browser.find_element_by_id('calibrationERRO').click()
            time.sleep(3)
            #只获取值，先不设置,默认三组
            calibration={}
            calibration_length = len(self.browser.find_element_by_id("dataList").find_elements_by_tag_name('tr'))
            for k in range(calibration_length):
                calibration[k]=(self.browser.find_element_by_id("dataList").find_elements_by_tag_name('tr')[k].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('input')[0].get_attribute('value'),\
                                self.browser.find_element_by_id("dataList").find_elements_by_tag_name('tr')[k].find_elements_by_tag_name('td')[3].find_elements_by_tag_name('input')[0].get_attribute('value'))
            

            self.browser.find_element_by_id('submitBtn').click()
            time.sleep(3)
            self.browser.find_element_by_id('doSubmit').click()
         
        title =[u"外设id",u"监控对象",u"传感器型号",u"波特率",u"滤波系数",u"补偿使能",u"奇偶校验",u"载重测量方法",u"传感器重量单位",u"空载阈值",\
                u"空载阈值偏差",u"轻载阈值",u"轻载阈值偏差",u"满载阈值",u"满载阈值偏差",u"超载阈值",u"超载阈值偏差"]    
        logtofile(logfile,"UI data:\n")
        for k in range(len(sensor_data)):
            logtofile(logfile,title[k]+" :"+str(sensor_data[k])+"\n")
            
        for key,value in calibration.items():
            logtofile(logfile,"calibration data:"+str(key)+":"+str(value)+"\n")    
        
        return [sensor_data,calibration]
    def send_load_parameter(self,browser,logfile,logtofile):
        # 点击下发参数
        self.browser = browser
        logtofile(logfile,"send the parameters\n")
        self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[2].click()
        
        
        
        
        
        
        
        
        
        