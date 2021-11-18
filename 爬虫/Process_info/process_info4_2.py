import os
import time
import urllib.request
from datetime import datetime

import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
from dataserver import Mysqldb

def get_page_url(url, header, cookies):

    sdasdasdf = requests.get(url, headers=header, cookies=cookies, verify=False)
    sdasdasdf.encoding = 'utf-8'
    return sdasdasdf.text,sdasdasdf.status_code

def file_download(fileurl,file_type,outdir):
    if ".jpg" in file_type or ".png" in file_type:
        jcookies = {
            'JSESSIONID': '2A540B5E46DB1CFFF06336E06070AD1D',
        }

        jheaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'If-None-Match': 'W/^\\^122057-1605519082082^\\^',
            'If-Modified-Since': 'Mon, 16 Nov 2020 09:31:22 GMT',
        }
    else:
        jcookies = {
            'JSESSIONID': '2A540B5E46DB1CFFF06336E06070AD1D',
        }

        jheaders = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'If-None-Match': 'W/^\\^122057-1605519082082^\\^',
            'If-Modified-Since': 'Mon, 16 Nov 2020 09:31:22 GMT',
        }
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    ft = "."+fileurl.split("/")[-1].split(".")[-1]
    if ft in file_type:
        filename = fileurl.split("/")[-1]
        print(filename)
        ffff = requests.get(fileurl, headers=jheaders, cookies=jcookies, verify=False)
        ofile = f"./{outdir}/{filename}"
        print(ofile)
        if os.path.exists(ofile):
            os.remove(ofile)
        if ffff.status_code == 200:
            with open(ofile, "wb") as f:
                f.write(ffff.content)
        else:
            print(f"下载失败: {fileurl}")
    else:
        print("已过滤")

def get_link_list():
    lists = ['htm/article/2018-12-19/12678.html','htm/article/2018-12-17/12676.html','htm/article/2018-12-16/12677.html','htm/article/2018-12-16/12675.html','htm/article/2018-12-15/12673.html','htm/article/2018-12-14/12672.html','htm/article/2018-12-14/12671.html','htm/article/2018-12-14/12670.html','htm/article/2020-12-19/12886.html','htm/article/2020-07-10/12865.html','htm/article/2020-03-06/12784.html','htm/article/2020-01-01/12763.html','htm/article/2019-10-08/12737.html','htm/article/2019-05-13/12710.html','htm/article/2019-03-06/12692.html','htm/article/2019-02-27/12690.html','htm/article/2018-12-21/12680.html','htm/article/2018-10-19/12619.html','htm/article/2018-03-16/12518.html','htm/article/2017-11-09/12443.html','htm/article/2017-03-15/12233.html','htm/article/2016-11-24/12186.html','htm/article/2018-11-12/12653.html','htm/article/2018-11-12/12652.html','htm/article/2018-11-11/12651.html','htm/article/2018-11-11/12650.html','htm/article/2018-11-10/12649.html','htm/article/2018-11-10/12648.html','htm/article/2018-11-09/12647.html','htm/article/2018-11-09/12646.html','htm/article/2018-11-08/12645.html','htm/article/2018-11-08/12644.html','htm/article/2018-11-07/12638.html','htm/article/2018-11-06/12637.html','htm/article/2018-11-05/12643.html','htm/article/2018-11-04/12642.html','htm/article/2018-11-03/12641.html','htm/article/2018-11-02/12640.html']
    return lists



if __name__ == '__main__':
    headers = {
    'Origin': 'http://fiddle.jshell.net',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Referer': 'http://fiddle.jshell.net/_display/',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    }

    url_list = [
        "http://sz.haedu.gov.cn/htm/portal/6.html",
        "http://sz.haedu.gov.cn/htm/portal/363.html",
        "http://sz.haedu.gov.cn/htm/portal/22.html",
        "http://sz.haedu.gov.cn/htm/portal/7.html",
        "http://sz.haedu.gov.cn/htm/portal/21.html",
        "http://sz.haedu.gov.cn/htm/portal/357.html",
        "http://sz.haedu.gov.cn/htm/portal/358.html",
        "http://sz.haedu.gov.cn/htm/portal/359.html",
        "http://sz.haedu.gov.cn/htm/portal/360.html",
        "http://sz.haedu.gov.cn/htm/portal/22.html",
    ]

    cookies = {
        'JSESSIONID': '2F6E23762847FE8FDDEF9E3DFFBD0416',
    }

    headers = {
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Referer': '',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    dbinfo = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': 'root',
        'port': 3306,
        'db': 'process_info',
        'charset': 'utf8',
        'use_unicode': True
    }
    basic_url = "http://sz.haedu.gov.cn/"
    db = Mysqldb(dbinfo)
    fl = db.select("select link from 教育网源数据")
    xp_field_location = "//div[@class='wz_title']//text()"
    xp_field_name = "//div[@class='tx_bt']/h2/text()"
    xp_field_info = "//div[@class='tx_fbt']/span/text()"
    xp_field_content = "/html/body/div[3]/div/div/div/div[2]/div[2]//text()"
    num = 0

    fl = get_link_list()

    for link in fl:
        url = basic_url+link
        print(url)
        html,sc = get_page_url(url,headers,cookies)
        if sc == 404:
            continue
        soup = BeautifulSoup(html, "html.parser")
        htttt = etree.HTML(html)
        try:
            arctype = htttt.xpath(xp_field_location)[-1]
        except:
            arctype = ""
        print(arctype)
        arctitle = htttt.xpath(xp_field_name)
        arcinfo2 = htttt.xpath(xp_field_info)
        arccontent = soup.find_all("div", class_="txt")
        # for a in arcinfo2:
        #     arcinfo += a+"|"
        del arcinfo2[-1:]
        try:
            arcinfo_t = arcinfo2[0]
        except:
            arcinfo_t = '2015-01-01 00:00:00'
        try:
            arcinfo_s = arcinfo2[1].replace("来源：","")
        except:
            arcinfo_s = None
        arccontent = str(arccontent).replace('\\r', '\r').replace('\\n', ' \n').replace('\\t', '\t').replace(']', '').replace('[',
                                                                                                          '').replace(
            '&nbsp;', '').replace(" ","").replace("\'","\"")
        arcinfo_t = str(time.mktime(datetime.strptime(arcinfo_t, '%Y-%m-%d %H:%M:%S').timetuple()))[:-2]
        insert_sql = f"""insert into arc_old_data_extra(arctype,arctitle,arcinfo_t,arcinfo_s,arccontent) VALUES('{arctype}','{arctitle[0]}',{arcinfo_t},'{arcinfo_s}','{arccontent}')"""
        db.execute(insert_sql)
