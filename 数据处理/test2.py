import re
import openpyxl
import pandas as pd


def sp(li):
    if len(li) == 0:
        return ""
    for i in li:
        return i


def sp_n(li):
    for i in range(len(li)):
        li[i] = li[i].replace("\n", "")
    return li


def fill_list(my_list: list, length, fill=None):  # 使用 fill字符/数字 填充，使得最后的长度为 length
    if len(my_list) >= length:
        return my_list
    else:
        return my_list + (length - len(my_list)) * [fill]

sss = []
with open("填空题.txt", "r", encoding="utf-8") as f:
    for line in f.readlines():
        title = line.split("ANSWER")[0]
        try:
            op = line.split("ANSWER")[1].lstrip("：").replace("\n", "")
        except:
            op = ""

        type = "填空题"
        fin_w = [type,title,op]
        sss.append(fin_w)

name = ["类型","题目","答案"]
test=pd.DataFrame(columns=name,data=sss)
test.to_csv("填空题.csv",encoding="GBK")


