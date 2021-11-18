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
with open("选择题.txt", "r") as f:
    for line in f.readlines():
        if line=="\n":
            continue
        title = line.split("A.")[0]
        select = line.split("答案")[1].replace("ANSWER","").replace("\n","")
        a_o =line.split("答案")[0].lstrip(line.split("答案")[0].split("A.")[0]).replace("ANSWER","")
        op_li = sp_n(re.split(r"[A-F][.]", a_o))
        del op_li[0]
        if len(select) > 1:
            题型 = "多选"
        else:
            题型 = "单选"
        答案 = select
        题目 = title
        选项 = fill_list(op_li, 6, "")
        选项.insert(0, 题目)
        选项.insert(0, 题型)
        选项.append(答案)
        sss.append(选项)
name = ["类型","题目","A选项","B选项","C选项","D选项","E选项","F选项","答案"]
test=pd.DataFrame(columns=name,data=sss)
print(test)
test.to_csv("选择题.csv",encoding="GBK")


