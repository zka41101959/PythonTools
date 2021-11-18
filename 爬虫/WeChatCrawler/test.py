import json
import time

import pymysql
import requests


def get_sqlConn():
  try:
    conn = pymysql.connect(
      # host='localhost',
      host="127.0.0.1",
      port=3306,
      user='root',
      password=123456,
      db='info',
      charset='utf8'
    )
    print('数据库连接成功！')
    return conn
  except:
    print('error')

def insert_wechat_content(wechat_name, title, content_url, cover, source_url, source_name, datetime):
  try:
    conn = get_sqlConn()
    cur = conn.cursor()
    #     sql = "INSERT INTO anjuke_beijing_onenum_all_house(house_name,house_plate,house_url,create_time) VALUES (%s,%s,%s,%s)"
    sql = """INSERT INTO info(wechat_name,title,content_url,cover,source_url,source_name,datetime) VALUES (%s,%s,%s,%s,%s,%s,%s)""" % (
    wechat_name, title, content_url, cover, source_url, source_name, datetime)
    print("微信公众号插入sql:%s" % sql)
    cur.execute(sql)
    conn.commit()
    print('插入数据成功！')
  except Exception as e:
    print('插入发生数据错误！ERROR:%s' % e)
    conn.rollback()  # 回滚
  finally:
    cur.close()
    conn.close()
  print('操作数据库完毕！')

def select_wechat_content(title):
  conn = get_sqlConn()
  cur = conn.cursor()
  try:
    sql = "SELECT EXISTS(SELECT 1 FROM info WHERE title=%s)" % title
    print("微信公众号查询SQL：%s" % sql)
    cur.execute(sql)
    return cur.fetchall()[0]
  except Exception as e:
    print('查询发生数据错误！ERROR:%s' % e)
    conn.rollback()
  cur.close()
  conn.close()

def get_parms(u):
    data = u.split("&")
    parms = {}
    for i in data:
        d = i.split("=")
        parms[d[0]] = d[1]
    parms['__biz'] = parms['__biz'] + "=="
    print(parms)
    return parms

def get_wx_article(u, wechat_name, index=0, count=10):
    """
  :param u:  抓包获取的请求地址，不要/mp/profile_ext?
  :param wechat_name: 公众号名，往数据库保存使用
  :param index: 翻页
  :param count: 每次请求条数
  :return:
  """
    offset = (index + 1) * count
    url = "http://mp.weixin.qq.com/mp/profile_ext?"

    params = get_parms(u)
    params['offset'] = offset
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Cookie': 'rewardsn=; wxtokenkey=777; wxuin=1583816706; devicetype=Windows10; version=62070141; lang=zh_CN; pass_ticket=n9Zz/2GEUA9SBL/LVdK8uLAPMwNph3rMVVksmgD0xrMOstqSxkc+aMVRVnfNAC9M; wap_sid2=CILAnPMFElw5Z0w3VXRGdjhNTlF4Ujd0YXFUSjM0MUpkSGFkcUdHTC0wa08tcUR3aEtWZElvcGRwTnUtUjllbHRTU3ctZ0JJQkR0RW1TZjgwNVZZd1RCaTMwNkZSd1lFQUFBfjCjgIDtBTgNQJVO'
    }
    response = requests.get(url=url, params=params, headers=headers)
    print(response.text)
    resp_json = response.json()
    if resp_json.get('errmsg') == 'ok':
        resp_json = response.json()
        # 是否还有分页数据， 用于判断return的值
        can_msg_continue = resp_json['can_msg_continue']
        # 当前分页文章数
        msg_count = resp_json['msg_count']
        general_msg_list = json.loads(resp_json['general_msg_list'])
        list = general_msg_list.get('list')
        print(list, "**************")
        wechat_name = wechat_name
        wechat_name = "'{}'".format(wechat_name)
        for i in list:
            print("=====>%s" % i)
            if 'app_msg_ext_info' not in i:  # 有特殊的公众号没有app_msg_ext_info字段，如果没有就跳过
                continue
            app_msg_ext_info = i['app_msg_ext_info']
            # 标题
            title = app_msg_ext_info['title']
            title = "'{}'".format(title)
            # 文章地址
            content_url = app_msg_ext_info['content_url']
            content_url = "'{}'".format(content_url)
            # 封面图
            cover = app_msg_ext_info['cover']
            cover = "'{}'".format(cover)
            # 转载路径
            source_url = app_msg_ext_info['source_url']
            source_url = "'{}'".format(source_url)

            # 转载公众号
            source_name = app_msg_ext_info['author']
            source_name = "'{}'".format(source_name)

            # 发布时间
            datetime = i['comm_msg_info']['datetime']
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datetime))
            datetime = "'{}'".format(datetime)

            print(title, content_url)
            print(source_url, source_name)
            print(cover, datetime)
            if select_wechat_content(title) == 1:  # 防止数据重复
                print("数据已经存在")
            else:
                insert_wechat_content(wechat_name, title, content_url, cover, source_url, source_name, datetime)

        if can_msg_continue == 1:
            return True
        return False
    else:
        print('获取文章异常...')
        return False

if __name__ == '__main__':
    index = 0
    # u = "action=getmsg&__biz=MzU0NDQ2OTkzNw==&f=json&offset=17&count=10&is_ok=1&scene=&uin=MTU4MzgxNjcwNg%3D%3D&key=5a37b8e9f2933463aa4c791beaedc828c781ae48f9a58c2067595d03e2a4da3d43e47af1b87aea58849a45838a5cd1375e69afd980a0562d3327ff9a7227684fa872ad73ae54f8d9ae5b2392595e0a4d&pass_ticket=n9Zz%2F2GEUA9SBL%2FLVdK8uLAPMwNph3rMVVksmgD0xrMOstqSxkc%2BaMVRVnfNAC9M&wxtoken=&appmsg_token=1030_sVyKhffomeHucF5TrTgG3CyPO9kX-j3obN4DNg~~&x5=0&f=json"
    u = ""
    while 1:
        print(f'开始抓取公众号第{index + 1} 页文章.')
        flag = get_wx_article(u, "测试公众号", index=index)
        # 防止和谐，暂停8秒
        time.sleep(8)
        index += 1
        if not flag:
            print('公众号文章已全部抓取完毕，退出程序.')
            break

        print(f'..........准备抓取公众号第{index + 1} 页文章.')