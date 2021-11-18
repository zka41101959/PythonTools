import math
import os
import requests
from dataserver import Mysqldb
from lxml import etree
from bs4 import BeautifulSoup


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


def file_download(fileurl,file_type_list,outdir):
    image_type_list = [".jpg",".png"]
    video_type_list = [".flv",".mp4"]
    itlb = [True for l in image_type_list if (l in file_type_list)]
    vtlb = [True for l in video_type_list if (l in file_type_list)]
    if itlb:
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
    elif vtlb:
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
    pass
    # while (True):
    #     try:
    #         proxy = get_proxy()
    #         response = requests.get("http://www.baidu.com", timeout=2, verify=False)
    #         if response.status_code == 200:
    #             break
    #     except Exception as e:
    #         print("Error")
    # xhtml = etree.HTML(response.text)
    # ele1 = xhtml.xpath("")
    # soup = BeautifulSoup(response.text, "html.parser")
    # arccontent = soup.find_all("div", class_="txt")


