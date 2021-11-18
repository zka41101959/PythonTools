import os, sys, requests
import json, re, time
from retrying import retry
from contextlib import closing


class DouYin:
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        }

    def hello(self):
        print("开始获取数据")
        return self

    def get_video_urls(self, sec_uid, type_flag='p'):
        user_url_prefix = 'https://www.iesdouyin.com/web/api/v2/aweme/post' if type_flag == 'p' else 'https://www.iesdouyin.com/web/api/v2/aweme/like'
        print('---解析视频链接中...\r')
        i = 0
        result = []
        while result == []:
            i = i + 1
            print('---正在第 {} 次尝试...\r'.format(str(i)))
            user_url = user_url_prefix + '/?sec_uid=%s&count=2000' % (sec_uid)
            response = self.get_request(user_url)
            html = json.loads(response.content.decode())
            if html['aweme_list'] != []:
                result = html['aweme_list']
        nickname = None
        count=0
        video_list = []
        for item in result:
            count+=1
            if nickname is None:
                nickname = item['author']['nickname'] if re.sub(r'[\/:*?"<>|]', '',
                                                                item['author']['nickname']) else None
            try:
                cover = item['video']['origin_cover']['url_list'][0]
            except:
                cover = ""
            video_list.append({
                'video_name': "{}.".format(str(count))+re.sub(r'[\/:*?"<>|\n]', '', item['desc']) if item['desc'] else "{}.".format(str(count))+'无标题' + str(int(time.time())),
                'video_cover': cover,
                'video_url': "https://www.douyin.com/video/{}".format(item["statistics"]["aweme_id"]),
                'video_download_url': item['video']['play_addr']['url_list'][0]
            })

        return nickname, video_list

    @retry(stop_max_attempt_number=3)
    def get_request(self, url, params=None):
        if params is None:
            params = {}
        response = requests.get(url, params=params, headers=self.headers, timeout=10)
        assert response.status_code == 200
        return response

    @retry(stop_max_attempt_number=3)
    def post_request(self, url, data=None):
        if data is None:
            data = {}
        response = requests.post(url, data=data, headers=self.headers, timeout=10)
        assert response.status_code == 200
        return response

    def run(self,sec_uid):
        type_flag = 'p' # 上传的视频
        nickname, video_list = self.get_video_urls(sec_uid, type_flag)
        return nickname,video_list



def getdata(username):
    from dataserver import Mysqldb
    dbinfo = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': '123456',
        'port': 3306,
        'db': 'info',
        'charset': 'utf8',
        'use_unicode': True
    }
    mysql = Mysqldb(dbinfo)
    sel_sql = f"select username,sec_id from dy_user_sec where username like '%{username}%';"
    username_and_sec_list = mysql.select(sel_sql)
    print(sel_sql)
    for username,sec_id in username_and_sec_list:
        charge_spider = DouYin().hello()
        nickname,video_list = charge_spider.run(sec_uid = sec_id)
        sc = sec_id
        res_tuple = (nickname, sc, video_list)
    return res_tuple

print(getdata("陈陈Chelsea"))





