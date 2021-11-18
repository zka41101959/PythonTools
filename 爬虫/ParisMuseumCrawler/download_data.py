import random
from multiprocessing import Process

from tqdm import tqdm

from dataserver import Mysqldb
import os
import urllib.request

dbinfo = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '123456',
    'port': 3306,
    'db': 'info',
    'charset': 'utf8',
    'use_unicode': True
}

def download_data(url,filemane,savepath,re_name_list):
    if not os.path.exists(savepath):
        print("输出文件夹不存在,已新建")
        os.makedirs(savepath)
    else:
        os.chmod(savepath, 777)
        if savepath=="./":
            savepath = "./"
        else:
            savepath = (savepath + "/")
        if filemane in re_name_list:
            filemane = filemane+f"_{str(random.randint(0, 5000))}"
        with urllib.request.urlopen(url, timeout=30) as response, open(savepath+filemane+".jpg", 'wb') as f_save:
            f_save.write(response.read())
            f_save.flush()
            f_save.close()
            print("成功下载：%s"%(filemane+".jpg"))

def download_data2(url,filemane,savepath,re_name_list):

    if not os.path.exists(savepath):
        print("输出文件夹不存在,已新建")
        os.makedirs(savepath)
    try:
        filemane = filemane.replace("?", "").replace("__","_")
        os.chmod(savepath, 777)
        if savepath == "./":
            savepath = "./"
        else:
            savepath = (savepath + "/")
        if filemane in re_name_list:
            filemane = filemane + f"_{str(random.randint(0, 5000))}"
        print(savepath + filemane + ".zip")
        with urllib.request.urlopen(url, timeout=30) as response, open(savepath + filemane + ".zip",
                                                                       'wb') as f_save:
            f_save.write(response.read())
            f_save.flush()
            f_save.close()
            print("成功下载：%s" % (filemane + ".zip"))
    except Exception as e:
        print("出错了: "%e)

def get_image_url_and_re(keyword):
    image_only = Mysqldb(dbinfo).select(
        f"SELECT DISTINCT name,image_link FROM `all_url` where classify like '%{keyword}%' and image_link !='' and zip_link = '';")
    old_list,repeat_elements = [],[]
    [old_list.append(name) for name,image_link in image_only]
    new_list = list(set(old_list))
    new_list.sort(key=old_list.index)
    for i in range(len(new_list)):
        if old_list[i] == new_list[i]:
            continue
        else:
            repeat_elements.append(old_list[i])
            del old_list[i]
    re_name_list = list(set(repeat_elements))
    return image_only,re_name_list

def get_zip_url_and_re(keyword):
    zip_only = Mysqldb(dbinfo).select(f"SELECT DISTINCT  name,zip_link FROM `all_url` where classify like '%{keyword}%' and zip_link !='';")
    old_list,repeat_elements = [],[]
    [old_list.append(name) for name,zip_link in zip_only]
    new_list = list(set(old_list))
    new_list.sort(key=old_list.index)
    for i in range(len(new_list)):
        if old_list[i] == new_list[i]:
            continue
        else:
            repeat_elements.append(old_list[i])
            del old_list[i]
    re_name_list = list(set(repeat_elements))
    return zip_only,re_name_list


def download_file(res_only, re_name_list,tag):
    if tag=="image":
        for name, image_link in res_only:
            image = eval(image_link)[0]
            download_data(image,name,"./image_file",re_name_list)
    elif tag =="zip":
        for name, zip_link in tqdm(res_only):
            try:
                download_data2(zip_link, name, "./zip_file", re_name_list)
            except Exception as e:
                print("出错了: %s，%s"%(e,name))
                continue



def test():
    # image_only, re_name_list = get_image_url_and_re()
    # download_file(image_only, re_name_list,"image")

    # zip_only, re_name_list = get_zip_url_and_re()
    # download_file(zip_only, re_name_list, "zip")
    pass





def d_image_multhread(keyword):
    image_only, re_name_list = get_image_url_and_re(keyword)
    if len(image_only) == 0:
        print("There is no task need to do !!!")
        return
    else:
        print("There is [%s] task need to do !!!" % len(image_only))
        process_count, worksprocess = 15, []
        process_task_num = len(image_only) / process_count
        if process_task_num == 0:
            process_count, process_task_num = len(image_only), 1
        for i in range(process_count):
            if i != process_count - 1:
                source_list = image_only[int(i * process_task_num):int((i + 1) * process_task_num)]
            else:
                source_list = image_only[int(i * process_task_num):]
            work = Process(target=download_file, args=(source_list, re_name_list,"image"))
            work.start()
            worksprocess.append(work)
        for work in worksprocess:
            work.join()
        del worksprocess

def d_zip_multhread(keyword):
    zip_only, re_name_list = get_zip_url_and_re(keyword)
    if len(zip_only) == 0:
        print("There is no task need to do !!!")
        return
    else:
        print("There is [%s] task need to do !!!" % len(zip_only))
        process_count, worksprocess = 30, []
        process_task_num = len(zip_only) / process_count
        if process_task_num == 0:
            process_count, process_task_num = len(zip_only), 1
        for i in range(process_count):
            if i != process_count - 1:
                source_list = zip_only[int(i * process_task_num):int((i + 1) * process_task_num)]
            else:
                source_list = zip_only[int(i * process_task_num):]
            work = Process(target=download_file, args=(source_list, re_name_list,"zip"))
            work.start()
            worksprocess.append(work)
        for work in worksprocess:
            work.join()
        del worksprocess

if __name__ == '__main__':
    keyword = "Méaulle, Fortuné Louis"
    d_image_multhread(keyword)
    # d_zip_multhread(keyword)