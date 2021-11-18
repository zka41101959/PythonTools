import math
import os.path
import time
from multiprocessing import Process
import shutil
import requests
from dataserver import Mysqldb

dbinfo = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': 'root',
    'port': 3306,
    'db': 'process_info',
    'charset': 'utf8',
    'use_unicode': True
}

cookies = {
    'areaid': '41',
    'cityid': '4101',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
    'sec-ch-ua-mobile': '?0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
url = """https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&colleges_level=&department=&doublehigh=&dual_class=&f211=&f985=&is_doublehigh=&is_dual_class=&is_single=2&local_batch_id=&local_province_id=41&local_type_id=2&nature=&page={1}&province_id=&request_type=1&school_type=&signsafe=&size=10&special_id={0}&type=&uri=apidata/api/gk/special/school&year=2020"""


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

def get_list():
    db3 = Mysqldb(dbinfo)
    return db3.select("select * from ygzy_jyzxyxk;")

def path_to_file(path):
    path = path.split("\\")
    return path[len(path) - 1]

def fullpath_to_path_and_filename(path,suffix=None):
    temp = path
    path = path.split("\\")
    return temp.rstrip(path[len(path) - 1]), path[len(path) - 1].rstrip(suffix)


def get_file_list_from_path(path, suffix=None, exclude=None):
    allfile = []
    for root, dirs, files in os.walk(path):
        for file in files:
            c = os.path.splitext(file)[1]
            if c == suffix:
                allfile.append(os.path.join(root, file))
    if exclude and exclude != []:
        [[allfile.remove(i) for ex in exclude if path_to_file(i) in ex]
         for i in allfile]
    return allfile

def alive_json():
    file_li = get_file_list_from_path(r'D:\Develop\PythonTools\爬虫\Process_info\school_information',suffix='.json')
    ali_s = []
    for i in file_li:
        path,file_code = fullpath_to_path_and_filename(i,suffix='.json')
        ali_s.append(file_code)
    return  ali_s


def test(li):
    ali_s = alive_json()
    for pro in li:

        url = 'https://static-data.eol.cn/www/2.0/school/{0}/info.json'
        (school_id,) = pro[-13:-12]
        if school_id in ali_s:
            continue
        print(school_id)
        if school_id in []:
            continue
        print("school_id: ", school_id)
        page = 1
        url_marge_t = url.format(school_id)
        while (True):
            try:
                proxy = get_proxy()
                js = requests.get(url_marge_t, headers=headers, proxies=proxy, timeout=1)
                print(js.json()['data'])
                with open(f"./school_information/{school_id}.json", "w", encoding="utf-8") as f:
                    f.write(str(js.json()['data']))
                break
            except Exception as e:
                print(e)

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
            work = Process(target=test, args=(source_list, ))
            work.start()
            worksprocess.append(work)
        for work in worksprocess:
            work.join()
        del worksprocess



if __name__ == '__main__':
    get_circle_address()
    # url_list = get_list()
    # test(url_list)