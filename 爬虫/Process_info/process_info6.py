import os
import re
import time
from bs4 import BeautifulSoup
from lxml import etree

from dataserver import Mysqldb


def get_s(ppp):
    ft = "." + ppp.split("/")[-1].split(".")[-1]
    return ft


dbinfo = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': 'root',
    'port': 3306,
    'db': 'sizheng',
    'charset': 'utf8',
    'use_unicode': True
}


def get_path_info(path):
    (fp, tfn) = os.path.split(path)
    (fn0, es) = os.path.splitext(tfn)
    return fp, tfn, fn0, es


db = Mysqldb(dbinfo)
all_i = db.select("select aid,content,litpic from ey_article_content")
num = 0
l = ['/uploads/static/image/icon_doc.gif', '</uploads/static/image/icon_pdf.gif',
     '/uploads/static/image/icon_xls.gif', '/uploads/static/image/icon_default.png',
     '/uploads/static/image/icon_doc.gif', '/uploads/static/image/icon_mp3.gif']
for (aid, content, seo) in all_i:
    soup = BeautifulSoup(content, "html.parser")
    seo_data = soup.find_all("img")
    html = etree.HTML(content)
    ps = html.xpath("//img/@src")
    if ps:
        print(ps)
            # content = str(content).replace(str(img), "附件: ")
            # print(True)
    # print(content)
    # us = f"UPDATE ey_article_content SET content='{content}' WHERE aid={aid}"
    # db.execute(us)
        # if str(img)=='<img src="/uploads/static/image/icon_pdf.gif"/>':
    # seo_e = soup.getText().replace('\n', '')[0:50]
    # if not seo_e[0:1] =="<":
    #     us = f"UPDATE ey_article_content SET seo='{seo_e}' WHERE aid={aid}"
    #     db.execute(us)

    #     new_str = "/uploads/static/video/"+v['src'].split("/")[-1:][0]
    #     new_fin = new_fin.replace(old_str,new_str)

    # for img in img_soup_list:
    #     konwn_list = ['<img src="/uploads/static/image/icon_doc.gif"/>',
    #                   '<img src="/uploads/static/image/icon_doc.gif"/>',
    #                   '<img src="/uploads/static/image/icon_pdf.gif"/>',
    #                   '<img src="/uploads/static/image/icon_xls.gif"/>',]
    #     if str(img) in konwn_list:
    #         continue
    #     try:
    #         old_str = img.attrs['src']
    #         new_str = "/uploads/static/image/" + old_str.split("/")[-1:][0]
    #         new_fin = new_fin.replace(old_str,new_str)
    #     except:
    #         pass
    # print(new_fin)
    # us = f"UPDATE ey_article_content SET litpic='{image_adress}' WHERE aid={aid}"
    # db.execute(us)

    # fl = re.findall("<a href=(.*?)>",content)
    # fin_str = content
    # for f in fl:
    #     f = f.replace("\"","")
    #     if get_s(f) in ['.doc','.pdf','.docx','.xls','.xlsx','.mp3']:
    #         old_str=f
    #         print(old_str)
    # new_str=f.replace("http://sz.haedu.gov.cn/","").replace("http://www.haedu.gov.cn/UserFiles/File/","").split("/")[-1:][0]
    # if get_s(f) == ".mp3":
    #     path = "/uploads/static/video/"
    # else:
    #     path = "/uploads/static/file/"
    # pat = path+new_str
    # content = content.replace(old_str,pat)
    # fin_str = content.replace("http://sz.haedu.gov.cn/shared/ueditor/dialogs/attachment/fileTypeImages/",
    #                           "/uploads/static/image/").replace(
    #     "/shared/ueditor/dialogs/attachment/fileTypeImages", "/uploads/static/image")

    # print(f"update ey_article_content set content='{fin_str}' where aid={aid}")
    # else:
    # print("已过滤")
    # continue
    # fin_str = fin_str.replace("\\n","")
    # us = f"UPDATE ey_article_content SET content='{fin_str}' WHERE aid={aid}"
    # db.execute(f"UPDATE ey_article_content SET content='{fin_str}' WHERE aid={aid}")
