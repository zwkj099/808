# -*- coding: utf-8 -*-
import time
# from splinter import Browser
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

from selenium.webdriver.support.select import Select

reload(sys)
sys.setdefaultencoding('utf8')
class oil_management(object):
    def __init__(self):
        pass
        #self.browser = webdriver.Firefox()
    def set_oil_parameter(self,calibration_data,browser,vnum,logfile,logtofile):
        
        self.browser = browser
        
        # 油量管理id
        time.sleep(5)
        self.browser.find_element_by_id("a03ff712-9755-11e6-ae22-56b6b6499611").click()
        # 油量管理设置id
        time.sleep(3)
        self.browser.find_element_by_id("a66ee712-9755-11e6-ae22-56b6b6499611").click()
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
             
        if self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[6].text.find(u"主油箱")!=-1:  
            self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].\
            find_elements_by_tag_name('button')[0].click()
        else:
            self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[2].\
            find_elements_by_tag_name('button')[0].click()           
        
        if buttontext==("修改1").decode("utf-8"):
            pass

        else:
            print "设置"
            time.sleep(8)
            
            #获取监控对象名称
            plate_number = self.browser.find_element_by_id("brand").get_attribute('value')
            no=0
            if self.browser.find_element_by_id("TabFenceBox").get_attribute("class")=="active":
                no = 41
            else:
                no = 42              
            
            # 点击油箱型号下拉框
            self.browser.find_element_by_id("home1").find_elements_by_tag_name('div')[0].find_elements_by_tag_name('div')[0].find_elements_by_tag_name('div')[0].\
                find_elements_by_tag_name('div')[0].find_elements_by_tag_name('button')[0].click()
            #选择油箱型号，选第2个 
            time.sleep(3)
            self.browser.find_elements_by_class_name("bssuggest-row")[1].click()
            
            time.sleep(3)
            # 展开隐藏参数
            self.browser.find_element_by_id("tankBasisInfo").click()
            time.sleep(3)
              
            #oil info   
                    
            oil_type = self.browser.find_element_by_id("oilBoxId").get_attribute('value')
            ##oil_shape:select 1：长方体，2：圆柱形，3：D形，4：椭圆形
            shape1Hidden = self.browser.find_element_by_id("shape1Hidden").get_attribute('value')
            box_length = self.browser.find_element_by_id("boxLength").get_attribute('value')
            box_width = self.browser.find_element_by_id("width").get_attribute('value')
            box_height = self.browser.find_element_by_id("height").get_attribute('value')     
            box_tick = self.browser.find_element_by_id("thickness").get_attribute('value')
            theory_volume = self.browser.find_element_by_id("theoryVolume").get_attribute('value')
            actual_volume = self.browser.find_element_by_id("realVolume").get_attribute('value')      
            
            #选择传感器下拉框
#             self.browser.find_element_by_id("home1").find_elements_by_tag_name('div')[4].find_elements_by_tag_name('div')[1]\
#                     .find_elements_by_tag_name('div')[0].find_elements_by_tag_name('div')[0].find_elements_by_tag_name('button')[0].click()
                    
#             self.browser.find_elements_by_tag_name('input-group-btn')[1].find_elements_by_tag_name('button')[0].click()  
            self.browser.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/div[2]/div/div[2]/div/div[2]/div[4]/div[1]/div/div/button").click()
            
            time.sleep(2)        
            #选择传感器,选择第2个
            self.browser.find_element_by_id("sensorchance").find_elements_by_tag_name("tr")[1].click()
            
            time.sleep(2)
            #展开传感器参数
            self.browser.find_element_by_id("sensorBasisInfo").click() 
           
            # sensor info
            sensor_type = self.browser.find_element_by_id("sensorNumber").get_attribute('value')
            sensor_length = self.browser.find_element_by_id("sensorLength").get_attribute('value')
            baudrate = self.browser.find_element_by_id("baudRate").get_attribute('value')
            filterfactor = self.browser.find_element_by_id("filteringFactor").get_attribute('value')
            compensate = self.browser.find_element_by_id("compensationCanMake").get_attribute('value')
            oddEvenCheck = self.browser.find_element_by_id("oddEvenCheck").get_attribute('value')  
            

            group_num,autouploadtime,output_k,output_b,addoiltime,addoil,seepoiltime,seepoil=calibration_data
            
            time.sleep(3)        
            #输入个性参数，标定数据
            self.browser.find_element_by_id('calibrationSets').clear()
            self.browser.find_element_by_id('calibrationSets').send_keys(group_num)
            time.sleep(3) 
            #选择默认上传时间，默认选择第2项
            Select(self.browser.find_element_by_id('automaticUploadTime')).select_by_index(int(autouploadtime))
            time.sleep(2) 
            self.browser.find_element_by_id('outputCorrectionCoefficientK').clear()
            time.sleep(2)
            self.browser.find_element_by_id('outputCorrectionCoefficientK').send_keys(output_k)
            time.sleep(3) 
            self.browser.find_element_by_id('outputCorrectionCoefficientB').clear()
            time.sleep(2)
            self.browser.find_element_by_id('outputCorrectionCoefficientB').send_keys(output_b)
            time.sleep(3) 
            self.browser.find_element_by_id('addOilTimeThreshold').clear()
            time.sleep(2)
            self.browser.find_element_by_id('addOilTimeThreshold').send_keys(addoiltime)
            time.sleep(3) 
            self.browser.find_element_by_id('addOilAmountThreshol').clear()
            time.sleep(2)
            self.browser.find_element_by_id('addOilAmountThreshol').send_keys(addoil)
            time.sleep(3) 
            self.browser.find_element_by_id('seepOilTimeThreshold').clear()
            time.sleep(2)
            self.browser.find_element_by_id('seepOilTimeThreshold').send_keys(seepoiltime)
            time.sleep(3) 
            self.browser.find_element_by_id('seepOilAmountThreshol').clear()
            time.sleep(2)
            self.browser.find_element_by_id('seepOilAmountThreshol').send_keys(seepoil)
            time.sleep(3) 
            #获取个性参数
            group_num1= self.browser.find_element_by_id('calibrationSets').get_attribute('value')
            autouploadtime1=self.browser.find_element_by_id('automaticUploadTime').get_attribute('value')
            output_k1=self.browser.find_element_by_id('outputCorrectionCoefficientK').get_attribute('value')
            output_b1=self.browser.find_element_by_id('outputCorrectionCoefficientB').get_attribute('value')
            addoiltime1=self.browser.find_element_by_id('addOilTimeThreshold').get_attribute('value')
            addoil1=self.browser.find_element_by_id('addOilAmountThreshol').get_attribute('value')
            seepoiltime1=self.browser.find_element_by_id('seepOilTimeThreshold').get_attribute('value')
            seepoil1=self.browser.find_element_by_id('seepOilAmountThreshol').get_attribute('value')
            
            
            sensor_data=[plate_number,no,oil_type,shape1Hidden,box_length,box_width,box_height,box_tick,theory_volume,actual_volume,\
                         sensor_type,sensor_length,baudrate,filterfactor,compensate,oddEvenCheck,group_num1,autouploadtime1,output_k1,\
                         output_b1,addoiltime1,addoil1,seepoiltime1,seepoil1]
            #点击计算标定按钮
            self.browser.find_element_by_id('calculateBtn').click()
            time.sleep(3)
            
            self.browser.find_element_by_xpath('/html/body/div[8]/div[3]/a[1]').click()
            
            time.sleep(2)
            #查看标定，返回标定组数
            self.browser.find_element_by_xpath('/html/body/div[1]/div/div/form/div[2]/div[2]/div/div[2]/div/div[2]/div[11]/span/a[3]').click()
            
            time.sleep(3)
            calibration={}

            for k in range(1,int(group_num1)+1):
                calibration[k-1]=(self.browser.find_elements_by_name("oilLevelHeights")[k].get_attribute('value'),self.browser.find_elements_by_name("oilValues")[k].get_attribute('value'))
                
            
            self.browser.find_element_by_id('submitBtn').click()
            time.sleep(3)
            self.browser.find_element_by_id('doSubmitBtn').click()
 
        title =[u"监控对象",u"外设id",u"油箱型号",u"油箱形状",u"长度",u"宽度",u"高度",u"壁厚",u"理论容积",u"油箱容量",u"传感器型号",u"传感器长度",u"波特率",u"滤波系数",\
                u"补偿使能",u"奇偶校验", u"标定数组",u"自动上传时间",u"输出修正系数K",\
                u"输出修正系数B",u"加油时间阈值",u"加油量阈值",u"漏油时间阈值",u"漏油量阈值"]    
        logtofile(logfile,"UI data:\n")
        for k in range(len(sensor_data)):
            logtofile(logfile,title[k]+" :"+str(sensor_data[k])+"\n")
             
#         for data in sensor_data:
#             logtofile(logfile,"sensor_data:"+str(data)+"\n")
        for key,value in calibration.items():
            logtofile(logfile,"calibration data:"+str(key)+":"+str(value)+"\n")  
                       
        return [sensor_data,calibration]
    def send_oil_parameter(self,browser,logfile,logtofile):
        # 点击下发参数
        self.browser = browser    
        logtofile(logfile,"send the parameters\n")    
        self.browser.find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('button')[2].click()
        
        
        
        
        
        
        
        
        
        