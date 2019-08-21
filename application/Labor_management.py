# -*- coding: utf-8 -*-
import time
# from splinter import Browser
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

from selenium.webdriver.support.select import Select

reload(sys)
sys.setdefaultencoding('utf8')
class labor_management(object):
    def __init__(self):
        pass
        #self.browser = webdriver.Firefox()
    def set_labor_parameter(self,calibration_data,browser,sensor_index,count,vnum,logfile,logtofile):
        
        self.browser = browser
        
        if count==0:
            #工时管理id
            time.sleep(5)
            self.browser.find_element_by_id("81649806-838d-11e6-ae22-56b6b6499611").click()
            # 工时管理设置id
            time.sleep(3)
            self.browser.find_element_by_id("7a4fc0c6-838e-11e6-ae22-56b6bf499611").click()
            time.sleep(5)
            # 搜索框输入桂A00002
            self.browser.find_element_by_id('simpleQueryParam').send_keys(vnum)
            
            time.sleep(5)
            # 点击搜索按钮
            self.browser.find_element_by_id('search_button').click()
        
        lasttimethreshold,Wavecalculatio_number,smoothingFactor,baudRateThreshold,Wavecalculatio_time,speedThreshold,thresholdVoltage=calibration_data
        
        time.sleep(3)
        # 点击第一个按钮设置、修改

        
        buttontext = self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2]. \
             find_elements_by_tag_name('button')[0].text
        if self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[6].text.find("1#")!=-1:    
            self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[0].click()
        else:
            self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[0].click()
        
        if buttontext==("修改1").decode("utf-8"):
            pass

        else:
            print "设置"
            time.sleep(5)
            
            #获取监控对象名称
            plate_number = self.browser.find_element_by_id("vehicleBrand").get_attribute('value')            
            
            if self.browser.find_element_by_id("egine2Title").get_attribute("class")=="active":
                self.browser.find_element_by_id("engin1A").click()
                time.sleep(3)

                
            time.sleep(3)
            #选择传感器下拉框 
            self.browser.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/button").click()
            
            time.sleep(2)        
            #选择传感器,选择第1个
            self.browser.find_elements_by_class_name("bssuggest-row")[int(sensor_index)].click()
            
            time.sleep(2)
           
            # sensor info
            sensor_type = self.browser.find_element_by_id("sensorId1").get_attribute('value')
            detectionMode = self.browser.find_element_by_id("detectionMode").get_attribute('value')
            filterfactor = self.browser.find_element_by_name("filterFactor").get_attribute('value')
            compensate = self.browser.find_element_by_name("compensate").get_attribute('value')
            oddEvenCheck = self.browser.find_element_by_name("oddEvenCheck").get_attribute('value')  
            baudrate = self.browser.find_element_by_name("baudRate").get_attribute('value')
            

            time.sleep(3)        
            #输入个性参数，标定数据

            time.sleep(2)
            if detectionMode.find("电压比较式")!=-1:
                self.browser.find_element_by_id('lastTimeYa').clear()
                time.sleep(2)
                self.browser.find_element_by_id('lastTimeYa').send_keys(lasttimethreshold)
                self.browser.find_element_by_id('thresholdVoltage').clear()
                time.sleep(2)
                self.browser.find_element_by_id('thresholdVoltage').send_keys(thresholdVoltage)
                time.sleep(2)
                lastTimeYa=self.browser.find_element_by_id('lastTimeYa').get_attribute('value')
                time.sleep(2)
                
            elif detectionMode.find("油耗波动式")!=-1:
                self.browser.find_element_by_id('lastTimeLiu').clear()
                time.sleep(2)
                self.browser.find_element_by_id('lastTimeLiu').send_keys(lasttimethreshold)
                time.sleep(2)
                self.browser.find_element_by_id('baudRateCalculateNumber').clear()
                time.sleep(2)
                self.browser.find_element_by_id('baudRateCalculateNumber').send_keys(Wavecalculatio_number)
                time.sleep(3) 
                self.browser.find_element_by_id('smoothingFactor').clear()
                time.sleep(2)
                self.browser.find_element_by_id('smoothingFactor').send_keys(smoothingFactor)
                time.sleep(2) 
                self.browser.find_element_by_id('baudRateThreshold').clear()
                time.sleep(2)
                self.browser.find_element_by_id('baudRateThreshold').send_keys(baudRateThreshold)
                time.sleep(2) 
                #选择波动计算时段
                Select(self.browser.find_element_by_id('baudRateCalculateTimeScope')).select_by_index(int(Wavecalculatio_time))
                time.sleep(2) 
                self.browser.find_element_by_id('speedThreshold').clear()
                time.sleep(2)
                self.browser.find_element_by_id('speedThreshold').send_keys(speedThreshold)
                lastTimeYa=self.browser.find_element_by_id('lastTimeLiu').get_attribute('value')
                
            else:
                self.browser.find_element_by_id('lastTimeWf').clear()
                time.sleep(2)
                self.browser.find_element_by_id('lastTimeWf').send_keys(lasttimethreshold)
                time.sleep(2)
                lastTimeYa=self.browser.find_element_by_id('lastTimeWf').get_attribute('value')
            
            
            #获取个性参数
            sensor_data=[]
            
            sensor_data=[plate_number,sensor_type,filterfactor,compensate,detectionMode,oddEvenCheck,baudrate,lastTimeYa]
            
            if detectionMode.find("电压比较式")!=-1:
                thresholdVoltage1=self.browser.find_element_by_id('thresholdVoltage').get_attribute('value')
                sensor_data.append(thresholdVoltage1)
            elif detectionMode.find("油耗波动式")!=-1:
                valuelist =['baudRateCalculateNumber','smoothingFactor','baudRateThreshold','baudRateCalculateTimeScope','speedThreshold']
                for value in valuelist:
                    sensor_data.append(self.browser.find_element_by_id(value).get_attribute('value'))


        time.sleep(3)
        self.browser.find_element_by_id('doSubmit').click()
            
        logtofile(logfile,"UI data\n")   
        for data in sensor_data:
            logtofile(logfile,"UI sensor_data:"+str(data)+"\n")
            
        return sensor_data
    
    def send_labor_parameter(self,browser,logfile,logtofile):
        # 点击下发参数

        self.browser = browser  
        logtofile(logfile,"send the parameters\n")  
        tdtext = self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[6].text   
        if tdtext.find("1#发动机")!=-1: 
            self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].\
            find_elements_by_tag_name('button')[2].click()
        else:
            self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[2].\
            find_elements_by_tag_name('button')[2].click()
            
        
        
        
        
        
        
        
        
        
        