# -*- coding: utf-8 -*-
import time
# from splinter import Browser
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

from selenium.webdriver.support.select import Select

reload(sys)
sys.setdefaultencoding('utf8')
class oilwear_management(object):
    def __init__(self):
        pass
        #self.browser = webdriver.Firefox()
    def set_oilwear_parameter(self,calibration_data,browser,vnum,logfile,logtofile):
        
        self.browser = browser
        
        # 油耗管理id
        time.sleep(5)
        self.browser.find_element_by_id("fc87a5b8-7d62-11e6-ae22-56b6b6499611").click()
        # 油耗管理设置id
        time.sleep(3)
        self.browser.find_element_by_id("94712ca2-7d7a-11e6-ae22-56b6b6499611").click()
        time.sleep(5)
        # 搜索框输入桂A00002
        self.browser.find_element_by_id('simpleQueryParam').send_keys(vnum)
        
        time.sleep(5)
        # 点击搜索按钮
        self.browser.find_element_by_id('search_button').click()
        

        
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
            plate_number = self.browser.find_element_by_id("brand").get_attribute('value')            
            
            #选择传感器下拉框 
            self.browser.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/div[2]/div/div/div/div[2]/div/div/div/button").click()
            
            time.sleep(2)        
            #选择传感器,选择第1个
            self.browser.find_elements_by_class_name("bssuggest-row")[0].click()
            
            time.sleep(2)
           
            # sensor info
            sensor_type = self.browser.find_element_by_id("fluxSensor").get_attribute('value')
            baudrate = self.browser.find_element_by_id("baudRate").get_attribute('value')
            filterfactor = self.browser.find_element_by_id("filterFactor").get_attribute('value')
            compensate = self.browser.find_element_by_id("compensate").get_attribute('value')
            parity = self.browser.find_element_by_id("parity").get_attribute('value')  
            

            autouploadtime,output_k,output_b=calibration_data
            
            time.sleep(3)        
            #输入个性参数，标定数据

            #选择默认上传时间，默认选择第2项
            Select(self.browser.find_element_by_id('autoUploadTime')).select_by_index(int(autouploadtime))
            time.sleep(2) 
            
            self.browser.find_element_by_id('outputCorrectionK').clear()
            time.sleep(2)
            self.browser.find_element_by_id('outputCorrectionK').send_keys(output_k)
            time.sleep(3) 
            self.browser.find_element_by_id('outputCorrectionB').clear()
            time.sleep(2)
            self.browser.find_element_by_id('outputCorrectionB').send_keys(output_b)
            time.sleep(3) 
            #获取个性参数
            autouploadtime1=self.browser.find_element_by_id('autoUploadTime').get_attribute('value')
            output_k1=self.browser.find_element_by_id('outputCorrectionK').get_attribute('value')
            output_b1=self.browser.find_element_by_id('outputCorrectionB').get_attribute('value')

            
            
            sensor_data=[plate_number,sensor_type,baudrate,filterfactor,compensate,parity,autouploadtime1,output_k1,output_b1]

            time.sleep(3)
#             self.browser.find_element_by_id('doSubmitBtn').click()
            
            while True:
                time.sleep(2)

                try:
                    if self.browser.find_element_by_xpath("/html/body/div[8]/div[3]/a[1]"):
                        
                        self.browser.find_element_by_xpath("/html/body/div[8]/div[3]/a[1]").click()
                        continue
                except:
                    print "except 1"
                
                time.sleep(1)    
                try:
                    print "ok"
                    if self.browser.find_element_by_id('doSubmit'):
                        self.browser.find_element_by_id('doSubmit').click()
                        break
                except:
                    print "except 2"

                break
                
#                 if self.browser.is_element_not_present_by_xpath("/html/body/div[8]/div[3]/a[1]")!=True:
#                     self.browser.find_element_by_xpath("/html/body/div[8]/div[3]/a[1]").click()
#                     continue
#                     
#                 elif self.browser.is_element_not_present_by_id('doSubmitBtn')!=True:
#                     self.browser.find_element_by_id('doSubmitBtn').click()
#                     break
#                 else:
#                     break
        title =[u"监控对象",u"传感器型号",u"波特率",u"滤波系数",u"补偿使能",u"奇偶校验",u"自动上传时间",u"输出修正系数K",u"输出修正系数B"]    
        logtofile(logfile,"UI data:\n")
        for k in range(len(sensor_data)):
            logtofile(logfile,title[k]+" :"+str(sensor_data[k])+"\n")
                        
#         for data in sensor_data:
#             logtofile(logfile,"sensor_data:"+str(data)+"\n")      
            
        return sensor_data
    def send_oilwear_parameter(self,browser,logfile,logtofile):
        # 点击下发参数
        self.browser = browser   
        logtofile(logfile,"send the parameters\n")     
        self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[2].click()
        
        
        
        
        
        
        
        
        
        