# -*- coding: utf-8 -*-
import time
# from splinter import Browser
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

from selenium.webdriver.support.select import Select

reload(sys)
sys.setdefaultencoding('utf8')
class reversible_management(object):
    def __init__(self):
        pass
        #self.browser = webdriver.Firefox()
    def set_reversible_parameter(self,calibration_data,browser,vnum,logfile,logtofile):
        
        self.browser = browser
        
        #湿度监测id
        time.sleep(5)
        self.browser.find_element_by_id("32e16f92-622b-11e7-907b-a6006ad3dba0").click()
        # 湿度监测设置id
        time.sleep(3)
        self.browser.find_element_by_id("9722bc7a-622d-11e7-907b-a6006ad3dba0").click()
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
            sensor_type = self.browser.find_element_by_id("sensorNumber").get_attribute('value')
            compensate = self.browser.find_element_by_id("compensate").get_attribute('value')
            

            autouploadtime,output_k,output_b=calibration_data
            
            time.sleep(3)        
            #输入个性参数，标定数据

            #选择默认上传时间，默认选择第2项
            Select(self.browser.find_element_by_id('autoTime')).select_by_index(int(autouploadtime))
            time.sleep(2) 
            
            self.browser.find_element_by_id('correctionFactorK').clear()
            time.sleep(2)
            self.browser.find_element_by_id('correctionFactorK').send_keys(output_k)
            time.sleep(3) 
            self.browser.find_element_by_id('correctionFactorB').clear()
            time.sleep(2)
            self.browser.find_element_by_id('correctionFactorB').send_keys(output_b)      
            time.sleep(2) 

            
            #获取个性参数
            autouploadtime1=self.browser.find_element_by_id('autoTime').get_attribute('value')
            output_k1=self.browser.find_element_by_id('correctionFactorK').get_attribute('value')
            output_b1=self.browser.find_element_by_id('correctionFactorB').get_attribute('value')

            
            
            sensor_data=[plate_number,sensor_type,compensate,autouploadtime1,output_k1,output_b1]

            time.sleep(3)
#             self.browser.find_element_by_id('doSubmit').click()

            while True:
                time.sleep(2)
                try:
                    if self.browser.find_element_by_xpath("/html/body/div[8]/div[3]/a[1]"):
                        
                        self.browser.find_element_by_xpath("/html/body/div[8]/div[3]/a[1]").click()
                        continue
                except:
                    print "no popup windows yet"
                
                time.sleep(1)    
                try:
                    if self.browser.find_element_by_id('doSubmit'):
                        self.browser.find_element_by_id('doSubmit').click()
                        break
                except:
                    print "except 2"

                break
        title =[u"监控对象",u"传感器型号",u"补偿使能",u"自动上传时间",u"输出修正系数K",u"输出修正系数B"] 
           
        logtofile(logfile,"UI data:\n")
        for k in range(len(sensor_data)):
            logtofile(logfile,title[k]+" :"+str(sensor_data[k])+"\n")
            
#         for data in sensor_data:
#             logtofile(logfile,"sensor_data:"+str(data)+"\n")
#                         
        return sensor_data
    
    def send_reversible_parameter(self,browser,logfile,logtofile):
        # 点击下发参数
        self.browser = browser   
        logtofile(logfile,"send the parameters\n")     
        self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[2].click()
        
        
        
        
        
        
        
        
        
        