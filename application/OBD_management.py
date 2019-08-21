# -*- coding: utf-8 -*-
import time
# from splinter import Browser
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

from selenium.webdriver.support.select import Select

reload(sys)
sys.setdefaultencoding('utf8')
class obd_management(object):
    def __init__(self):
        pass
        #self.browser = webdriver.Firefox()
    def set_obd_parameter(self,calibration_data,browser,vnum,logfile,logtofile):
        
        self.browser = browser
        
        #obd监测id
        time.sleep(5)
        self.browser.find_element_by_id("0c60fc12-71d9-4dc2-a773-eb568a5f7777").click()
        # obd设置id
        time.sleep(3)
        self.browser.find_element_by_id("0c60fc30-71d9-4dc2-a773-eb568a5f9472").click()
        time.sleep(5)
        # 搜索框输入桂A00002
        self.browser.find_element_by_id('simpleQueryParam').send_keys(vnum)
        
        time.sleep(5)
        # 点击搜索按钮
        self.browser.find_element_by_id('search_button').click()
        

        autouploadtime=calibration_data
        
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
            plate_number = self.browser.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/div[1]/div/div/div[1]/input").get_attribute('value')            
            
            #选择车型分类下拉框 ，默认选第2个
            Select(self.browser.find_element_by_id('deviceType')).select_by_index(1)  
            time.sleep(2)
            #选择发动机类型 ，默认选第2个
            Select(self.browser.find_element_by_id('typeList')).select_by_index(1)  
            time.sleep(2)
            self.browser.find_element_by_id('time').clear()
            time.sleep(2)
            self.browser.find_element_by_id('time').send_keys(autouploadtime)
            time.sleep(2)
                       
            # sensor info
            device_type = self.browser.find_element_by_id("deviceType").get_attribute('value')
            typeList = self.browser.find_element_by_id("typeList").get_attribute('value')
            vehicleTypeId = self.browser.find_element_by_id("vehicleTypeId").get_attribute('value')
            autouploadtime1=self.browser.find_element_by_id('time').get_attribute('value')
            
            
            sensor_data=[plate_number,device_type,typeList,vehicleTypeId,autouploadtime1]

            time.sleep(3)
            self.browser.find_element_by_id('doSubmit').click()
            
        title =[u"监控对象",u"车型分类",u"车型名称",u"车型",u"OBD采集间隔"] 
           
        logtofile(logfile,"UI data:\n")
        for k in range(len(sensor_data)):
            logtofile(logfile,title[k]+" :"+str(sensor_data[k])+"\n")
            
#         for data in sensor_data:
#             logtofile(logfile,"sensor_data:"+str(data)+"\n")
                        
        return sensor_data
    
    def send_obd_parameter(self,browser,logfile,logtofile):
        # 点击下发参数
        self.browser = browser   
        logtofile(logfile,"send the parameters\n")     
        self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[2].click()
        
        
        
        
        
        
        
        
        
        