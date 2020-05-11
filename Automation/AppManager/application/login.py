# -*- coding: utf-8 -*-
import time
# from splinter import Browser
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class login(object):
    def __init__(self):
        pass
    def login(self,url,browser,username,password):
        # browser = webdriver.Firefox()
        browser.get(url)
        browser.find_element_by_id('email').send_keys(username)

        browser.find_element_by_id('tg_password').send_keys(password)
        time.sleep(5)
        # 获取滑块
#         element = browser.find_element_by_id('label')
#         ActionChains(browser).click_and_hold(on_element=element).perform()
#         ActionChains(browser).move_to_element_with_offset(to_element=element, xoffset=300, yoffset=0).perform()
#         ActionChains(browser).release(on_element=element).perform()
        time.sleep(5)

        # click the button of login
        browser.find_element_by_id('login_ok').click()
        time.sleep(5)
        
        # 应用管理id
        time.sleep(5)
        browser.find_element_by_id('9f5ea704-6a90-11e6-8b77-86f30ca893d3').click()

    def quit_browser(self,browser):
        browser.quit()
       


