import os
import urllib.request
import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
from dataserver import Mysqldb

def get_page_url(url, header, cookies):

    sdasdasdf = requests.get(url, headers=header, cookies=cookies, verify=False)
    sdasdasdf.encoding = 'utf-8'
    return sdasdasdf.text

def file_download(fileurl,file_type_list,outdir):
    if ".jpg" in file_type_list or ".png" in file_type_list:
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
    if ft in file_type_list:
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
    # llx = "//div[@class='list_menu']/ul/li/a/@href"
    # for lanss in url_list:
    #     response = requests.get(lanss, headers=headers, cookies=cookies,
    #                             verify=False)
    #     response.encoding = 'utf-8'
    #     html = etree.HTML(response.text)
    #     lanlist = html.xpath(llx)
    #     print(lanlist)
    #     url_list.append(lanlist)
    # localtion = "//div[@class='wz_title']//text()"
    # page_num = "//div[@class='manu']//text()"
    # page_pss = ""
    # basic_url = "http://sz.haedu.gov.cn/htm/portal/{0}{1}.html"
    # list_list = []

    # for lanss in url_list:
    #     response = requests.get(lanss, headers=headers, cookies=cookies, verify=False)
    #     response.encoding = 'utf-8'
    #     html = etree.HTML(response.text)
    #     locat = html.xpath(localtion)
    #     page_n = html.xpath(page_num)
    #     page_f = int(re.findall(r"共(.*?)页",page_n[0])[1])
    #     page_list = []
    #     if page_f > 1:
    #         page_list.append(lanss)
    #         basic_u = lanss.rstrip(".html")
    #         for i in range(1, page_f):
    #             ssn = basic_u + "_" + str(i)+".html"
    #             page_list.append(ssn)
    #         # d = get_page_url(fu,headers,cookies)
    #         list_list.extend(page_list)
    #     else:
    #         page_list.append(lanss)
    #         list_list.extend(page_list)
    # lpxp = "//div[@class='new_list b_new']/ul/li/a/@href"
    # fl = []
    # for list_page in list_list:
    #     dasfa = requests.get(list_page, headers=headers, cookies=cookies)
    #     dasfa.encoding = "utf-8"
    #     ht = etree.HTML(dasfa.text)
    #     fl.extend(ht.xpath(lpxp))
    # for ss in fl:
    #     db.execute(f"insert into 教育网源数据(`link`) VALUES ('{ss}')")
        # break
    basic_url = "http://sz.haedu.gov.cn/"
    db = Mysqldb(dbinfo)
    fl = db.select("select link from 教育网源数据")
    xp_field_location = "//div[@class='wz_title']//text()"
    xp_field_name = "//div[@class='tx_bt']/h2/text()"
    xp_field_info = "//div[@class='tx_fbt']/span/text()"
    xp_field_content = "/html/body/div[3]/div/div/div/div[2]/div[2]//text()"
    for (link,) in fl:
        # link = "http://sz.haedu.gov.cn/htm/article/2017-11-03/12438.html"
        url = basic_url+link
        # url = "http://sz.haedu.gov.cn/htm/article/2020-04-22/12808.html"
        html = get_page_url(url,headers,cookies)
        soup = BeautifulSoup(html, "html.parser")
        htttt = etree.HTML(html)
        arctype = htttt.xpath(xp_field_location)[-1]
        arctitle = htttt.xpath(xp_field_name)
        arcinfo2 = htttt.xpath(xp_field_info)
        arccontent = soup.find_all("div", class_="txt")
        # image = htttt.xpath("//div[@class='txt']//img/@src")
        video = htttt.xpath("//div[@class='txt']//video/@src")
        # document = htttt.xpath("//div[@class='txt']/p/a/@href")
        # print(document)
        # print(video)
        # break
        # print(location)
        for a in video:
            document_url = basic_url+a
            print(document_url)
            # file_download(document_url,[".mp3"],"video")
        # break

        # print(location[-1])
        # print(title)
        # print(info)
        # print(content)
        # print(image)
        # print(doc)
        # print(video)
        # break



