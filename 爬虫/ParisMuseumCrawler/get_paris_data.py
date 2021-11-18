import requests
from lxml import etree
from multiprocessing import Process
import time
from tqdm import tqdm
from dataserver import Mysqldb
from selenium import webdriver
import re
import urllib3
urllib3.disable_warnings()

dbinfo = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '123456',
    'port': 3306,
    'db': 'info',
    'charset': 'utf8',
    'use_unicode': True
}


def execute_cdp_cmd(self, cmd, cmd_args):
    return self.execute("executeCdpCommand", {
        'cmd': cmd,
        'params': cmd_args
    })['value']


def set_driver():
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches",
                                   ['enable-automation', 'enable-logging'])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('--disable-infobars')
    option.add_argument('--start-maximized')
    option.add_argument('--headless')
    driver = webdriver.Chrome(
        chrome_options=option,
        executable_path=
        "C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe"
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument", {
            "source":
            """
               Object.defineProperty(navigator, 'webdriver', {
                 get: () => undefined
               })
             """
        })
    return driver


def get_classify_list(driver, url):
    driver.get(url)
    page = driver.page_source
    try:
        url_list = re.findall(
            'class="auteur-complet"><a href="/fr/.*?">(.*?)</a>', page, re.S)
        return url_list
    except:
        return [""]


def get_image_list(driver, url):
    driver.get(url)
    page = driver.page_source
    try:
        h = etree.HTML(page)
        url_list = h.xpath(
            '//div[@class="fullscreen-button"]/@data-fullscreen-img')
        if len(url_list) >= 1:
            return url_list
        else:
            return ""
    except Exception as e:
        return ""


def get_res_json(url):
    html = requests.get(url,verify=False)
    html.encoding = 'utf-8'
    if html.status_code == 200:
        return html.text
    else:
        time.sleep(0.5)
        return html.text


def get_url(ser, table_name):
    url_tuple = ser.select("select url from `%s`;" % table_name)
    url_list, list2 = [], []
    [url_list.append((url, )) for url, in url_tuple]
    list2 = list(set(url_list))
    list2.sort(key=url_list.index)
    return list2

def replace_name(name):
    name = name.replace("\'", "_").replace("/", "_").replace(
        "\\",
        "_").replace("\"", "_").replace("[", "_").replace("]", "_").replace(
            " : ", "_").replace(", ", "_").replace(".", "_").replace(
                "(", "_").replace(")", "_").replace(" ", "_").replace(
                    "________", "_").replace("_______", "_").replace(
                        "______", "_").replace("_____", "_").replace(
                            "____", "_").replace("___",
                                                 "_").replace("__", "_")
    return name.strip("_")


def get_name_and_zip(url_list):
    update_link_sql = 'update `all_url`set name=%s, file_type=%s, zip_link=%s, image_link=%s, classify=%s where url=%s;'

    # print("任务总数: %d" % len(url_list))
    data_ls = []

    for page_url in tqdm(url_list):
        driver = set_driver()
        if len(data_ls) > 0:
            Mysqldb(dbinfo).executemany(update_link_sql, data_ls)
            data_ls = []
        try:
            image_link = ""
            html_f = etree.HTML(get_res_json(page_url))
            try:
                file_name = replace_name(
                    html_f.xpath("//div[@class='field-item even']/h1/text()")
                    [0])
            except:
                print("name dont exits")
                file_name = ""
            try:
                image_link, zip_link = "", ""
                zip_link = "https://www.parismuseescollections.paris.fr" + html_f.xpath(
                    "//a[@class='download-zip']//@href")[0]
                file_type = "zip"
            except:
                image_link, zip_link = "", ""
                print("zip_link dont exits")
                file_type = "image"
            finally:
                try:
                    image_link = str(get_image_list(driver, page_url))
                except Exception as e:
                    print("no image: %s" % e)
            try:
                classify_list = get_classify_list(driver, page_url)
                del classify_list[0]
                classify = str(classify_list)
            except:
                print("classify不存在")
                classify = ""
            if image_link == "" and zip_link == "":
                file_type = ""
            data_ls.append((file_name, file_type, zip_link, image_link,
                            classify, page_url))
            driver.close()
        except Exception as e:
            print("文件不存在,等待下次处理. 异常: %s" % e)
            driver.close()

    if data_ls:
        Mysqldb(dbinfo).executemany(update_link_sql, data_ls)
        data_ls = []


def get_list():
    task_table = "all_url"
    exits_sql = "show tables like '%s';" % task_table
    if Mysqldb(dbinfo).select(exits_sql):
        print("结果表已存在,后续会更新此表内容: %s" % task_table)
    else:
        print("创建结果表: %s" % task_table)
        task_table = create_res_tab(task_table)



    url_tuple = Mysqldb(dbinfo).select(
        f"SELECT url FROM {task_table} where `name`='' or `classify` = '';")
    # url_tuple = Mysqldb(dbinfo).select(
    #     f"SELECT url FROM {task_table} where file_type is null and zip_link is null and classify is null;")


    # url_tuple = Mysqldb(dbinfo).select(
    #     f"SELECT `url` FROM {task_table} WHERE zip_link!=''and image_link = '';"
    # )
    # print(url_tuple)
    url_list = []
    [url_list.append(url) for url, in url_tuple]
    return url_list


def create_res_tab(out_table_name):
    create_table(out_table_name)
    # table_name1 = "url_1"
    # insert_data(table_name1, out_table_name)
    # table_name2 = "url_hugo_2"
    # insert_data(table_name2, out_table_name)
    # table_name3 = "url_pesme_paul_emile"
    # insert_data(table_name3, out_table_name)
    return out_table_name


def create_table(table_name):
    sql = """
    CREATE TABLE `%s` (
        `id` int NOT NULL AUTO_INCREMENT,
        `url` varchar(500) DEFAULT NULL,
        `name` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
        `file_type` varchar(255) DEFAULT NULL,
        `zip_link` text DEFAULT NULL,
        `image_link` text DEFAULT NULL,
        `classify` varchar(255) DEFAULT NULL,
        `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT='hugo_url_TABLE';""" % table_name
    del_table_sql = """DROP TABLE `%s`;""" % table_name
    Mysqldb(dbinfo).execute(sql)


def insert_data(table_name, out_table_name):
    insert_sql = """insert into `""" + out_table_name + """`(url) VALUES(%s);"""
    url_tuple_list = get_url(Mysqldb(dbinfo), table_name)
    print(len(url_tuple_list))
    Mysqldb(dbinfo).executemany(insert_sql, url_tuple_list)


def get_circle_address():
    url_list = get_list()
    if len(url_list) == 0:
        print("There is no task need to do !!!")
        return
    else:
        print("There is [%s] task need to do !!!" % len(url_list))
        process_count, worksprocess = 10, []
        process_task_num = len(url_list) / process_count
        if process_task_num == 0:
            process_count, process_task_num = len(url_list), 1
        for i in range(process_count):
            if i != process_count - 1:
                source_list = url_list[int(i * process_task_num):int(
                    (i + 1) * process_task_num)]
            else:
                source_list = url_list[int(i * process_task_num):]
            work = Process(target=get_name_and_zip, args=(source_list, ))
            work.start()
            worksprocess.append(work)
        for work in worksprocess:
            work.join()
        del worksprocess


if __name__ == '__main__':
    get_circle_address()
