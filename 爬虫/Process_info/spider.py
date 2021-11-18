import json
import re
import requests
import datetime
from bs4 import BeautifulSoup
import os
from dataserver import Mysqldb
from multiprocessing import Process


def get_p():
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
    proxy, ip = get_p()
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
            proxy, ip = get_p()


def geda(url, headers):
    while (True):
        try:
            dd = requests.get(url, headers=headers, proxies=get_proxy(), timeout=1)
            if dd.status_code == 200:
                return dd.text
        except:
            dd = ""
        if dd:
            return dd.text


def replace_string(k, lll):
    for i in range(len(lll)):
        k = k.replace(lll[i], '')
    return k

def get_list():
    dbinfo = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': 'root',
        'port': 3306,
        'db': 'process_info',
        'charset': 'utf8',
        'use_unicode': True
    }
    db1 = Mysqldb(dbinfo)
    return db1.select("select id,school_name from school;")


def main(kkk):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    for (id, sn) in kkk:
        url = str('https://baike.baidu.com/item/' + sn)
        html = geda(url, headers)
        soup = BeautifulSoup(html, "lxml")
        div_list = soup.find_all('div', class_='basic-info J-basic-info cmn-clearfix')
        slslsl = [
            '</dt>',
            '</dd>',
            '<dd>',
            '<dt>',
            '</dl>',
            '<dl>',
            '</a>',
            '<br/>',
            '<div class="basicInfo-overlap">',
            '<dl class="basicInfo-block overlap">',
            '<dl class="basicInfo-block basicInfo-right">',
            '</div>',
            '</em>',
            '<em class="arrow arrow-bg">',
            '<em class="arrow arrow-border">',
            '<a class="toggle toCollapse">',
            '</sup>'
        ]
        sss = ""
        for i in div_list:
            i = replace_string(str(i), slslsl)
            i = re.sub('<a.*?>', "", i)
            i = re.sub('<sup.*?>', "", i)
            i = re.sub('<dt class="basicInfo-item name">', "|||", i)
            i = re.sub('<div class="basic-info J-basic-info cmn-clearfix">', "|||", i)
            i = re.sub('<dd class="basicInfo-item value">', "", i)
            i = re.sub('<dl class="basicInfo-block basicInfo-left">', "|||", i)
            sss += i
        with open(f"./sss/{id}.txt",'w',encoding='utf-8') as f:
            f.write(sss)



def get_circle_address():
    url_list = get_list()
    if len(url_list) == 0:
        print("There is no task need to do !!!")
        return
    else:
        print("There is [%s] task need to do !!!" % len(url_list))
        process_count, worksprocess = 20, []
        process_task_num = len(url_list) / process_count
        if process_task_num == 0:
            process_count, process_task_num = len(url_list), 1
        for i in range(process_count):
            if i != process_count - 1:
                source_list = url_list[int(i * process_task_num):int(
                    (i + 1) * process_task_num)]
            else:
                source_list = url_list[int(i * process_task_num):]
            work = Process(target=main, args=(source_list, ))
            work.start()
            worksprocess.append(work)
        for work in worksprocess:
            work.join()
        del worksprocess



if __name__ == '__main__':
    get_circle_address()

