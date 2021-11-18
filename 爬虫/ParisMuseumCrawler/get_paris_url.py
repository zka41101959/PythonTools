import requests
from lxml import etree
from lxml import html
from html.parser import HTMLParser

page_num = 4

# basic_url =
# 'https://www.parismuseescollections.paris.fr/fr/recherche/type/oeuvre/ET/auteur/Bayard%2C%20Emile%20Antoine?page={}'
# basic_url =
# 'https://www.parismuseescollections.paris.fr/fr/recherche/type/oeuvre/ET/musee/maison%20de%20victor%20hugo%20-%20hauteville%20house-18?page={}'
# basic_url = '?page={}'
# basic_url =
# 'https://www.parismuseescollections.paris.fr/fr/recherche/type/oeuvre/ET/auteur/Pesme%2C%20Paul%20Emile?page={}'
# basic_url =
# 'https://www.parismuseescollections.paris.fr/fr/recherche/auteur/Beaumont%2C%20Charles-Edouard%20de/type/oeuvre?limit=150&sort=score&page={}'
basic_url = 'https://www.parismuseescollections.paris.fr/fr/recherche/auteur/Gavarni%20%28Hippolyte%20Sulpice%20Guillaume%20Chevalier%2C%20dit%29/type/oeuvre?limit=300&sort=score&page={}'
# 测试添加url
front_url = 'https://www.parismuseescollections.paris.fr{}'
xp = "//div[contains(@class,'wrapper-results')]//article//a[1]/@href"

url_list_f = open("url.txt", "a+", encoding="utf-8")
all_url = []
for i in range(1, page_num + 1):
    html = requests.get(basic_url.format(i))
    # html = requests.get(basic_url)
    html.encoding = 'utf-8'
    html_f = etree.HTML(html.text)
    url_list = html_f.xpath(xp)
    url_list = list(set(url_list))
    print("当前为第 %s 页, 有 %s 条数据" % (i, len(url_list)))
    for j in range(len(url_list)):
        url_list[j] = front_url.format(url_list[j])
    for k in url_list:
        url_list_f.writelines(k + '\n')

        # 测试