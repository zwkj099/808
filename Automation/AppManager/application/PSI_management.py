# -*- coding: utf-8 -*-
import time
# from splinter import Browser
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

from selenium.webdriver.support.select import Select

reload(sys)
sys.setdefaultencoding('utf8')
class psi_management(object):
    def __init__(self):
        pass
        #self.browser = webdriver.Firefox()
    def set_psi_parameter(self,calibration_data,browser,vnum,logfile,logtofile):
        
        self.browser = browser
        
        #胎压监测id
        time.sleep(5)
        self.browser.find_element_by_id("66ea642b-a561-4049-8bf3-ae837fac73ef").click()
        # 胎压设置id
        time.sleep(3)
        self.browser.find_element_by_id("66ea642b-a561-4049-8bf3-ae837fac73e2").click()
        time.sleep(5)
        # 搜索框输入桂A00002
        self.browser.find_element_by_id('simpleQueryParam').send_keys(vnum)
        
        time.sleep(5)
        # 点击搜索按钮
        self.browser.find_element_by_id('search_button').click()
        

        autouploadtime,output_k,output_b,normalTirePressure,pressureImbalanceThreshold,slowLeakThreshold,\
            highTemperatureThreshold,lowVoltageThreshold,highVoltageThreshold,powerAlarmThreshold=calibration_data
        
        time.sleep(3)
        # 点击第一个按钮设置、修改

        buttontext = self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2]. \
             find_elements_by_tag_name('button')[0].text
        self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[0].click()
        if buttontext==("修改1").decode("utf-8"):
            pass

        else:
            print "设置"
            time.sleep(8)
            
            #获取监控对象名称
            plate_number = self.browser.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/div[1]/div/div[1]/div[1]/input[1]").get_attribute('value')            
            time.sleep(2)
            #选择轮胎数量，默认选第2个
            Select(self.browser.find_element_by_id('numberOfTires')).select_by_index(1)  
            time.sleep(2)   
                     
            #选择传感器下拉框 
            self.browser.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/button").click()
            time.sleep(2)        
            #选择传感器,选择第1个
            self.browser.find_elements_by_class_name("bssuggest-row")[0].click()
            time.sleep(2)            
                       
            tires_number = self.browser.find_element_by_id("numberOfTires").get_attribute('value')
            # sensor info
            sensor_type = self.browser.find_element_by_id("sensorNumber").get_attribute('value')
            filterfactor = self.browser.find_element_by_id("filterFactor").get_attribute('value')
            compensate = self.browser.find_element_by_id("compensate").get_attribute('value')
            
            #个性参数
            
            Select(self.browser.find_element_by_id('autoTime')).select_by_index(int(autouploadtime))

            time.sleep(2)  
            self.browser.find_element_by_id('correctionFactorK').clear()
            time.sleep(2)
            self.browser.find_element_by_id('correctionFactorK').send_keys(output_k)
            time.sleep(3) 
            self.browser.find_element_by_id('correctionFactorB').clear()
            time.sleep(2)
            self.browser.find_element_by_id('correctionFactorB').send_keys(output_b)

            self.browser.find_element_by_id('normalTirePressure').clear()
            time.sleep(2)
            self.browser.find_element_by_id('normalTirePressure').send_keys(normalTirePressure)
            time.sleep(3)
            self.browser.find_element_by_id('pressureImbalanceThreshold').clear()
            time.sleep(2)
            self.browser.find_element_by_id('pressureImbalanceThreshold').send_keys(pressureImbalanceThreshold)
            time.sleep(3) 
            self.browser.find_element_by_id('slowLeakThreshold').clear()
            time.sleep(2)
            self.browser.find_element_by_id('slowLeakThreshold').send_keys(slowLeakThreshold)
            self.browser.find_element_by_id('highTemperatureThreshold').clear()
            time.sleep(2)
            self.browser.find_element_by_id('highTemperatureThreshold').send_keys(highTemperatureThreshold)
            time.sleep(3) 
            self.browser.find_element_by_id('lowVoltageThreshold').clear()
            time.sleep(2)
            self.browser.find_element_by_id('lowVoltageThreshold').send_keys(lowVoltageThreshold)
            self.browser.find_element_by_id('highVoltageThreshold').clear()
            time.sleep(2)
            self.browser.find_element_by_id('highVoltageThreshold').send_keys(highVoltageThreshold)
            time.sleep(3) 
            self.browser.find_element_by_id('powerAlarmThreshold').clear()
            time.sleep(2)
            self.browser.find_element_by_id('powerAlarmThreshold').send_keys(powerAlarmThreshold)                        
         
            autouploadtime1=self.browser.find_element_by_id('autoTime').get_attribute('value')
            output_k1=self.browser.find_element_by_id('correctionFactorK').get_attribute('value')
            output_b1=self.browser.find_element_by_id('correctionFactorB').get_attribute('value')
            
            normalTirePressure1=self.browser.find_element_by_id('normalTirePressure').get_attribute('value')
            pressureImbalanceThreshold1=self.browser.find_element_by_id('pressureImbalanceThreshold').get_attribute('value')
            slowLeakThreshold1=self.browser.find_element_by_id('slowLeakThreshold').get_attribute('value')
            highTemperatureThreshold1=self.browser.find_element_by_id('highTemperatureThreshold').get_attribute('value')
            lowVoltageThreshold1=self.browser.find_element_by_id('lowVoltageThreshold').get_attribute('value')
            highVoltageThreshold1=self.browser.find_element_by_id('highVoltageThreshold').get_attribute('value')
            powerAlarmThreshold1=self.browser.find_element_by_id('powerAlarmThreshold').get_attribute('value')
            
            
            sensor_data=[plate_number,tires_number,sensor_type,filterfactor,compensate,autouploadtime1,output_k1,output_b1,\
                         normalTirePressure1,pressureImbalanceThreshold1,slowLeakThreshold1,highTemperatureThreshold1,\
                         lowVoltageThreshold1,highVoltageThreshold1,powerAlarmThreshold1]

            time.sleep(3)
            self.browser.find_element_by_id('doSubmit').click()
        title =[u"监控对象",u"轮胎数量",u"传感器型号",u"滤波系数",u"补偿使能",u"自动上传时间",u"输出修正系数K",u"输出修正系数B",\
                u"正常胎压值",u"胎压不平衡门限",u"慢漏气门限",u"低压阈值",u"高压阈值",u"高温阈值",u"传感器电量报警阈值"]
                
           
        logtofile(logfile,"UI data:\n")
        for k in range(len(sensor_data)):
            logtofile(logfile,title[k]+" :"+str(sensor_data[k])+"\n")
#             
#         for data in sensor_data:
#             logtofile(logfile,"sensor_data:"+str(data)+"\n")            
        return sensor_data
    
    def send_psi_parameter(self,browser,logfile,logtofile):
        # 点击下发参数
        self.browser = browser 
        logtofile(logfile,"send the parameters\n")       
        self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[2].click()
        
        
        
        
        
        
        
        
        
        