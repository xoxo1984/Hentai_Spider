# -*- coding: UTF-8 -*-

import requests, json
from const import LOCAL_COOKIES_FILE

def login_hentai(username, password):
    session = requests.Session()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }
    data = {
        'UserName': username,
        'CookieDate': '1',
        'b': 'd',
        'bt': 'pone',
        'PassWord': password,
    }
    cookies = {
        'ipb_member_id': '0',
        'ipb_pass_hash': '0',
    }
    try:
        r = session.post(url='http://forums.e-hentai.org/index.php?act=Login&CODE=01',
                         headers=headers, cookies=cookies, data=data)
        page_content = r.content.decode('utf-8')
        if 'captcha' not in page_content:
            if r.cookies.get_dict()['ipb_member_id'] != '0':
                # 保存cookies到本地
                local_cookies = {}
                local_cookies['ipb_member_id'] = r.cookies.get_dict()['ipb_member_id']
                local_cookies['ipb_pass_hash'] = r.cookies.get_dict()['ipb_pass_hash']
                with open(LOCAL_COOKIES_FILE, "w") as f:
                    f.write(json.dumps(local_cookies))
                print('login success, save cookies to local file')
            else:
                print('login fail, please check your username & password')
        else:
            print('login fail, CAPTCHA in login page, this program cannot handle it, please try later')
    except:
        print('login fail, please check the network')
