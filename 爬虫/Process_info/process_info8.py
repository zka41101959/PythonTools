import requests
from lxml import etree

for i in range(0,841,20):
    basic_url = "https://yz.chsi.com.cn/sch/?start={}".format(i)
    h = requests.get(basic_url)
    title = etree.HTML(h.text).xpath("//table[@class='ch-table']/tbody/tr/td[1]/a")
    edu = etree.HTML(h.text).xpath("//td[@class='ch-table-center'][1]")
    for j in range(len(title)):
        print(str(title[j].text).replace(" ","").replace("\n",""))
        print(edu[j].xpath('string(.)'))


    break