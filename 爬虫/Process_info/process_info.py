# -*- coding: utf-8 -*-
import os

import requests
from lxml import etree
from multiprocessing import Process
import time
from selenium.webdriver import ActionChains
from tqdm import tqdm

from dataserver import Mysqldb
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import urllib3

urllib3.disable_warnings()
driver = None

def add_enter_key(input_file_name):
    full_text = ""
    file = open(f"./{input_file_name}.txt",'r',encoding='utf-8')
    for line in file.readlines():
        full_text+=line+"|||"
    file.close()
    os.remove(f"./{input_file_name}.txt")
    return full_text

def execute_cdp_cmd(self, cmd, cmd_args):
    return self.execute("executeCdpCommand", {
        'cmd': cmd,
        'params': cmd_args
    })['value']

def set_driver():
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches",
                                   ['enable-automation', 'enable-logging'])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('--disable-infobars')
    option.add_argument('--start-maximized')
    # option.add_argument('--headless')
    driver = webdriver.Chrome(
        chrome_options=option,
        executable_path=
        "C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe"
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument", {
            "source":
            """
               Object.defineProperty(navigator, 'webdriver', {
                 get: () => undefined
               })
             """
        })
    return driver



def parse_data(url_list):
    dbinfo = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': 'root',
        'port': 3306,
        'db': 'process_info',
        'charset': 'utf8',
        'use_unicode': True
    }
    db = Mysqldb(dbinfo)
    iframename = 'youzyPartView'
    driver = set_driver()
    for j in tqdm(range(len(url_list))):
        # Gb_code, full_po, full_content, full_wwo, sayly_list, Professional_list, school_list = None
        print("url= {}".format(url_list[j]))
        driver.get(url_list[j])
        time.sleep(3)
        driver.switch_to.frame("youzyPartView")
        Gb_code = url_list[j].split("=")[1].replace("\n","")
        print(Gb_code)
        try:
            Professional_overview = driver.find_element_by_class_name("info-box").text
        except:
            Professional_overview = None
        try:
            content = driver.find_element_by_class_name("major-info-list").text
        except:
            content = None

        try:
            driver.find_element_by_id("tab-second").click()
            time.sleep(3)
            sayly_list = []
            Professional_list = []
            try:
                work_way = driver.find_element_by_xpath('//*[@id="scorllELe"]/div[4]/div/div[1]/p').text
                work_way_out = '就业方向\n' + work_way
            except:
                work_way_out = None
            try:
                sayly = driver.find_elements_by_css_selector(
                    '.small-majors .mainIndustries ul, .small-majors .mainRegions ul, .small-majors .salary-box ul')
                for k in sayly:
                    with open(f"./{Gb_code}_sayly.txt", 'w+', encoding='utf-8') as f:
                        f.write(str(k.text))
                    full_sayly = add_enter_key(Gb_code + '_sayly')
                    sayly_list.append(full_sayly)
            except:
                sayly_list = []
            try:
                Professional_1 = driver.find_elements_by_xpath('//*[@id="scorllELe"]/div[4]/div/div[3]/div[1]/div[3]')
            except:
                Professional_1 = []
            try:
                Professional_2 = driver.find_elements_by_xpath('//*[@id="scorllELe"]/div[4]/div/div[3]/div[2]/ul')
            except:
                Professional_2 = []
            try:
                Professional_3 = driver.find_elements_by_xpath('//*[@id="scorllELe"]/div[4]/div/div[3]/div[3]/ul')
            except:
                Professional_3 = []
            try:
                main_work_1 = '主要职业分布\n' + Professional_1[0].text
                with open(f"./{Gb_code}_zy1.txt", 'w+', encoding='utf-8') as f:
                    f.write(str(main_work_1))
                full_zy1 = add_enter_key(Gb_code + '_zy1')
                Professional_list.append(full_zy1)
            except:
                print("缺少部分数据")
            try:
                main_work_2 = '主要行业分布\n' + Professional_2[0].text
                with open(f"./{Gb_code}_zy2.txt", 'w+', encoding='utf-8') as f:
                    f.write(str(main_work_2))
                full_zy2 = add_enter_key(Gb_code + '_zy2')
                Professional_list.append(full_zy2)
            except:
                print("缺少部分数据")
            try:
                main_work_3 = '主要就业地区分布\n' + Professional_3[0].text
                with open(f"./{Gb_code}_zy3.txt", 'w+', encoding='utf-8') as f:
                    f.write(str(main_work_3))
                full_zy3 = add_enter_key(Gb_code + '_zy3')
                Professional_list.append(full_zy3)
            except:
                print("缺少部分数据")
        except:
            print("不存在第二页")
            work_way_out = []
            Professional_list = []

        time.sleep(1)
        try:
            driver.find_element_by_id("tab-third").click()
            time.sleep(1)
            js = "var q=document.getElementsByClassName('tzy-page')[0].scrollTop = 10000"  #
            for i in range(5):
                driver.execute_script(js)
                time.sleep(2)
            school_list = []
            school = driver.find_elements_by_css_selector('.el-row--flex.is-align-middle')
            for i in school:
                with open(f"./{Gb_code}_sc.txt", 'w+', encoding='utf-8') as f:
                    f.write(str(i.text))
                full_sc = add_enter_key(Gb_code + '_sc')
                school_list.append(full_sc)
        except:
            print("不存在第三页")
            school_list = None
        time.sleep(1)
        with open(f"./{Gb_code}.txt", 'w', encoding='utf-8') as f:
            f.write(str(content))
        full_content = add_enter_key(Gb_code)
        with open(f"./{Gb_code}_po.txt", 'w', encoding='utf-8') as f:
            f.write(str(Professional_overview))
        full_po = add_enter_key(Gb_code + '_po')
        with open(f"./{Gb_code}_wwo.txt", 'w', encoding='utf-8') as f:
            f.write(str(work_way_out))
        full_wwo = add_enter_key(Gb_code + '_wwo')

        insert_sql = f'''INSERT INTO `test` ( `Gb_code`, `Professional_overview`, `content`, `work_way_out`, `sayly_list`, `Professional_list`, `school_list` )
            VALUES("{Gb_code}", "{full_po}","{full_content}","{full_wwo}","{sayly_list}","{Professional_list}","{school_list}");'''
        db.execute(insert_sql)


def get_list():
    url_list = []
    with open('./more.txt','r',encoding='utf-8')as f:
        li = f.readlines()
        for url in li:
            url_list.append(url)
    return url_list


def get_circle_address():
    url_list = get_list()
    if len(url_list) == 0:
        print("There is no task need to do !!!")
        return
    else:
        print("There is [%s] task need to do !!!" % len(url_list))
        process_count, worksprocess = 5, []
        process_task_num = len(url_list) / process_count
        if process_task_num == 0:
            process_count, process_task_num = len(url_list), 1
        for i in range(process_count):
            if i != process_count - 1:
                source_list = url_list[int(i * process_task_num):int(
                    (i + 1) * process_task_num)]
            else:
                source_list = url_list[int(i * process_task_num):]
            work = Process(target=parse_data, args=(source_list, ))
            work.start()
            worksprocess.append(work)
        for work in worksprocess:
            work.join()
        del worksprocess

if __name__ == '__main__':
    get_circle_address()