import re
import time
import requests
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree

def execute_cdp_cmd(self, cmd, cmd_args):
    return self.execute("executeCdpCommand", {'cmd': cmd,'params': cmd_args})['value']

def set_driver():
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches",['enable-automation', 'enable-logging'])
    option.add_experimental_option('useAutomationExtension', False)
    # option.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030532)"')
    option.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030532)"')
    option.add_argument('--disable-infobars')
    option.add_argument('--start-maximized')
    # option.add_argument('--headless') # 无头模式
    # option.add_argument('--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data')
    driver = webdriver.Chrome(chrome_options=option,executable_path="C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe")
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source":"""Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
    driver.delete_all_cookies()
    return driver

def get_short_link(url):
    try:
        a, b = url.split('&chksm=')
        return a
    except:
        return url


def search_keyword(url):
    browser = set_driver()
    browser.get(url)
    try:
        for i in range(10000):
            element = browser.find_element_by_class_name("tips_wrp")
            ActionChains(browser).move_to_element(element).perform()
            time.sleep(1)
            browser.execute_script("window.scrollBy(0,500)")
            # end_ele = browser.find_element_by_class_name("tips js_no_more_msg")
    except:
        print("已完成")
        title_xp = "//div/h4"
        post_date_xp = "//div/p[2]/text()"
        temp_link_xp = "//span[@class='weui_media_hd js_media']/@hrefs"
        time.sleep(2)
        try:
            title_list = etree.HTML(browser.page_source).xpath(title_xp)
        except:
            title_list = []
        try:
            post_date_list = etree.HTML(browser.page_source).xpath(post_date_xp)
        except:
            post_date_list = []
        try:
            temp_link_list = etree.HTML(browser.page_source).xpath(temp_link_xp)
        except:
            temp_link_list = []
        final_data = []
        for i in range(len(title_list)):
            title_list[i] = title_list[i].text.lstrip().rstrip()
            try:
                final_data.append((title_list[i], post_date_list[i], temp_link_list[i]))
            except:
                print("缺失数据")
                continue
        browser.close()
        for i in final_data:
            print(i)
    finally:
        print("已完成")
        title_xp = "//div/h4"
        post_date_xp = "//div/p[2]/text()"
        temp_link_xp = "//span[@class='weui_media_hd js_media']/@hrefs"
        time.sleep(2)
        try:
            title_list = etree.HTML(browser.page_source).xpath(title_xp)
        except:
            title_list = []
        try:
            post_date_list = etree.HTML(browser.page_source).xpath(post_date_xp)
        except:
            post_date_list = []
        try:
            temp_link_list = etree.HTML(browser.page_source).xpath(temp_link_xp)
        except:
            temp_link_list = []
        final_data = []
        for i in range(len(title_list)):
            title_list[i] = title_list[i].text.lstrip().rstrip()
            try:
                final_data.append((title_list[i], post_date_list[i], temp_link_list[i]))
            except:
                print("缺失数据")
                continue
        browser.close()
        for i in final_data:
            print(i)


url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU3NDgxOTMzNA==&scene=124&uin=Mjk5MTczNDcwMQ%3D%3D&key=2a2066ee7128965bfc152efc29598c104dff12e2d6143ee5b909b27ea2a7d4ed559d832d24954d7420b6df4053e7904f4d6a2bb6b52afed7417222f72823a499a621a93eb189b78c44ae6c1d1a8977b5358ffe68c93edc5fb00058dda39f219570c3dc331d37280492968f0a0f64e382be421377652bbd086cb78f21b414f8af&devicetype=Windows+10+x64&version=63030532&lang=zh_CN&a8scene=7&pass_ticket=QUo6yfvhkHFyhPIjtrnzLOgJzP%2BwOBO4W9ieXaZHi2BJANBK7VxiPPX4PpNQedhF&fontgear=2"
search_keyword(url)







