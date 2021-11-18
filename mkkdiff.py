import re

import pandas as pd

def dftolist(df):
    end_list = []
    [end_list.append(i)for i in df.values]
    return end_list

if __name__ == '__main__':
    df = pd.read_excel('source.xlsx')
    data1 = pd.DataFrame(df,columns=['题号','A选项','B选项','C选项','D选项'])
    datanum_l = dftolist(data1["题号"])
    data_A_l = dftolist(data1["A选项"])
    data_B_l = dftolist(data1["B选项"])
    data_C_l = dftolist(data1["C选项"])
    data_D_l = dftolist(data1["D选项"])
    res_list = []
    fg = '_'
    for i in range(len(datanum_l)):
        res_select = str(data_A_l[i]).replace("\t","")+fg+ str(data_B_l[i]).replace("\t","")+fg + str(data_C_l[i]).replace("\t","") +fg+ str(data_D_l[i]).replace("\t","")
        res_list.append(res_select)
    res_d = {}
    for j in range(len(datanum_l)):
        res_d[datanum_l[j]] = res_list[j]
    print(res_d)
    res_d_2 = {
        "str":[1,2,3]
    }
    with open("compose.txt") as f:
        while True:
            line = f.readline().rstrip()
            try:
                pattern = re.compile(r'^\d+')
                id = re.findall(pattern, line)
                if re.findall(pattern, line) == []:
                    print(id)
            except:
                pass
            if not line:
                break
    # print(res_d_2)






# dataanswer = data1["A选项"]+data1["B选项"]+data1["C选项"]+data1["D选项"]
# for i in len():
#     print(data[i])
# print(type(data))

# df=pd.read_excel('source.xlsx')
# test_data=[]
# for i in df.index.values:
#     row_data=df.iloc[i,['题号','A选项','B选项','C选项','D选项']].to_dict()
#     test_data.append(row_data)
# print("最终获取到的数据是：{0}".format(test_data))
