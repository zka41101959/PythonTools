import requests

cookies = {
    'ua_id': 'lg9kWcFGXaOWaqY7AAAAAPAQruXqEACLVY7zT8tFG5M=',
    'rewardsn': '',
    'wxtokenkey': '777',
    'appmsg_token': '1132_xSh6oN^%^2BjFm5rm1qePf9Yq-CX1RGGMANHqyyu2hTEPJpjipdUP3Uxz4jgvQMEDoP6x_NaAH5qBanmLKsn',
    'wxuin': '2991734701',
    'lang': 'zh_CN',
    'devicetype': 'Windows10x64',
    'version': '63030532',
    'pass_ticket': 'PGtBb+w0GqmvnCFkYtWgSY6b7RGEhW5c0aYf7ON/593iPJoFmUbK5SG8q6ziU7VL',
    'wap_sid2': 'CK3/yJILEooBeV9IUG1ZQ1BRWTEtR28zc3pDck9MU2RXalZRMkpNNVc4clpsNXJoemtXcUg0a3VzeWRmM3BSX3phYm8wQmcyY2ZJMG1CLVlwcFhoN1E1N0NzQVBNUzM2ME93TmZjUjFjNl9yRXp5bHBsMnBudmt0LWwwZlliSUExTllZLXMwS19BQVhrb1NBQUF+MMW7wIoGOA1AlU4=',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
    'sec-ch-ua-mobile': '?0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'image',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://mp.weixin.qq.com/',
    'Pragma': 'no-cache',
}

params = (
    ('action', 'home'),
    ('__biz', 'MjM5ODIzNzk0NA=='),
    ('scene', '124'),
    ('uin', 'Mjk5MTczNDcwMQ^%^3D^%^3D'),
    ('key', 'addbe6622204c06a7c08c349388976ce4027b7a19dd06ab758fd8073181118a06c15a85a5bbcade2876560a3fec843332067ed44a8135a44c53ae6b46280bf58ccc06f841700dc5cbc704fada657bca33b46c36a073d2ebd52a3c7379b2e6821255c6c6ba8cc919f70064594f107d58644bf1ec0fbf83936e37db49e8f7deaa1'),
    ('devicetype', 'Windows 10 x64'),
    ('version', '63030532'),
    ('lang', 'zh_CN'),
    ('a8scene', '7'),
    ('pass_ticket', 'PGtBb^%^2Bw0GqmvnCFkYtWgSY6b7RGEhW5c0aYf7ON^%^2F593iPJoFmUbK5SG8q6ziU7VL'),
    ('fontgear', '2'),
)

response = requests.get('https://mp.weixin.qq.com/mp/profile_ext', headers=headers, params=params, cookies=cookies)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5ODIzNzk0NA==&scene=124&uin=Mjk5MTczNDcwMQ^%^3D^%^3D&key=addbe6622204c06a7c08c349388976ce4027b7a19dd06ab758fd8073181118a06c15a85a5bbcade2876560a3fec843332067ed44a8135a44c53ae6b46280bf58ccc06f841700dc5cbc704fada657bca33b46c36a073d2ebd52a3c7379b2e6821255c6c6ba8cc919f70064594f107d58644bf1ec0fbf83936e37db49e8f7deaa1&devicetype=Windows+10+x64&version=63030532&lang=zh_CN&a8scene=7&pass_ticket=PGtBb^%^2Bw0GqmvnCFkYtWgSY6b7RGEhW5c0aYf7ON^%^2F593iPJoFmUbK5SG8q6ziU7VL&fontgear=2', headers=headers, cookies=cookies)
print(response.text)