# import requests
import requests
from lxml import etree
from multiprocessing import Process
# import time
# from tqdm import tqdm
from dataserver import Mysqldb
from selenium import webdriver
# import re


# sql执行
dbinfo = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '123456',
    'port': 3306,
    'db': 'info',
    'charset': 'utf8',
    'use_unicode': True
}

Mysqldb(dbinfo).execute("sql")



# selenium样例
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
    option.add_argument('--headless') # 无头模式
    driver = webdriver.Chrome(chrome_options=option,
        executable_path=
        "C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe")
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
            """
               Object.defineProperty(navigator, 'webdriver', {
                 get: () => undefined
               })
             """
        })
    return driver

driver = set_driver()
res_list = etree.HTML(driver.page_source).xpath("")

def get_list():
    return list

def need_mul_way():
    pass
# 多线程样例
def multiprocessingProcess():
    url_list = get_list()
    if len(url_list) == 0:
        print("There is no task need to do !!!")
        return
    else:
        print("There is [%s] task need to do !!!" % len(url_list))
        process_count, worksprocess = 15, []
        process_task_num = len(url_list) / process_count
        if process_task_num == 0:
            process_count, process_task_num = len(url_list), 1
        for i in range(process_count):
            if i != process_count - 1:
                source_list = url_list[int(i * process_task_num):int((i + 1) * process_task_num)]
            else:
                source_list = url_list[int(i * process_task_num):]
            work = Process(target=need_mul_way, args=(source_list,))
            work.start()
            worksprocess.append(work)
        for work in worksprocess:
            work.join()
        del worksprocess


def gpw():
    api_url = "http://zka41101959.v4.dailiyun.com/query.txt?key=NPX020584R&word=&count=1&rand=true&ltime=120&norepeat=false&detail=false"
    try:
        p_o = requests.get(api_url, headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"},
                           timeout=1).text
    except:
        p_o = None
    ii = p_o.rsplit("\r\n")[0]
    proxyurl = "http://" + "zka41101959" + ":" + "ufo4322532" + "@" + ii
    proxies = {'http': proxyurl, 'https': proxyurl}
    return proxies, ii.split(":")[0]

def get_proxy():
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Connection': 'keep-alive'}
    proxy, ip = gpw()
    while (True):
        try:
            res = requests.get('http://whatismyip.akamai.com/', headers=head, proxies=proxy, timeout=1).text
        except:
            res = None
        if (str(ip) == str(res).replace("\n", "").replace("\r", "")):
            print(str(proxy) + " 可用")
            return proxy
        else:
            print(str(proxy) + " 不可用")
            proxy, ip = gpw()

print(get_proxy())