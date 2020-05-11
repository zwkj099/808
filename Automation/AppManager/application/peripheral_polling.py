# -*- coding: utf-8 -*-
import time
# from splinter import Browser
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')
class polling(object):
    def __init__(self):
        pass
        #self.browser = webdriver.Firefox()
    def set_polling_parameter(self,sensor_num,browser,times,count,vnum,logfile,logtofile):
        self.browser = browser
        if count==0:
#         # 应用管理id
#             time.sleep(5)
#             self.browser.find_element_by_id('9f5ea704-6a90-11e6-8b77-86f30ca893d3').click()
            # 传感器配置id
            time.sleep(3)
            self.browser.find_element_by_id('b296585a-339c-11e7-a919-92ebcb67fe33').click()
            # 外设轮询id
            time.sleep(3)
            self.browser.find_element_by_id('cdc11c04-339d-11e7-a919-92ebcb67fe33').click()
            time.sleep(5)
            # 搜索框输入桂A00002
            self.browser.find_element_by_id('simpleQueryParam').send_keys(vnum)
            
            time.sleep(5)
            # 点击搜索按钮
            self.browser.find_element_by_id('search_button').click()
        plate_number = ""
        sensor = ""
        num = int(sensor_num)
        timestr=int(times)
        time.sleep(3)
        # 点击第一个按钮设置、修改

        buttontext = self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2]. \
             find_elements_by_tag_name('button')[0].text
        self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[0].click()
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
            time.sleep(5)
            # 点击传感器下拉框
            self.browser.find_element_by_id('sensorOrTime').find_elements_by_tag_name('div')[0].find_elements_by_tag_name('div')[0].find_elements_by_tag_name \
                ('div')[0].find_elements_by_tag_name('div')[0].find_elements_by_tag_name('button')[0].click()
            time.sleep(5)
            # 选择传感器类型
            self.browser.find_element_by_id('sensorOrTime').find_elements_by_tag_name('div')[0].find_elements_by_tag_name('div')[0].find_elements_by_tag_name('div')[0] \
                .find_elements_by_tag_name('div')[0].find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0] \
                .find_elements_by_tag_name('tr')[num].click()
            time.sleep(5)
            try:
                self.browser.find_element_by_id("pollingTime_3").clear()
                # 输入轮询时间
                self.browser.find_element_by_id("pollingTime_3").send_keys(timestr)
                time.sleep(3)
                timestr = self.browser.find_element_by_id("pollingTime_3").get_attribute('value')
            except:
                
                self.browser.find_element_by_id("pollingTime").clear()
                # 输入轮询时间
                self.browser.find_element_by_id("pollingTime").send_keys(timestr)
                time.sleep(3)
                timestr = self.browser.find_element_by_id("pollingTime").get_attribute('value')
                
            plate_number =self.browser.find_element_by_id("brands").get_attribute('value')
            sensor = self.browser.find_element_by_id("sensorType").get_attribute('value')
#             timestr = self.browser.find_element_by_id("pollingTime").get_attribute('value')
            self.browser.find_element_by_id('doSubmits').click()
        logtofile(logfile,u"监控对象:"+plate_number+" \n\n"+u"传感器类型:"+sensor+"\n\n"+u"轮询时间:"+timestr+"\n\n")
        
        return [plate_number,sensor,timestr]
    def send_polling_parameter(self,browser,logfile,logtofile):
        # 点击下发参数
        self.browser = browser
        logtofile(logfile,u"send the parameters\n")
        self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[1].click()
        
        
        
        
        
        
        
        
        
        