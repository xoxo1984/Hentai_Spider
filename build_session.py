# -*- coding: UTF-8 -*-

import requests, os, json
from const import *


def build_session():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }
    session = requests.Session()
    session.headers.update(headers)

    if os.path.exists(LOCAL_COOKIES_FILE):
        # load local cookies
        print('load local cookies')
        with open(LOCAL_COOKIES_FILE, "r") as f:
            c = requests.cookies.RequestsCookieJar()
            local_cookies = json.loads(f.read())
            for key in local_cookies:
                c.set(key, local_cookies[key])
        session.cookies.update(c)
        # try local cookies
        r = session.get('https://e-hentai.org/home.php')
        if 'E-Hentai.org Login' in r.content.decode('utf-8'):
            print('fail to connect hentai')
            session = False
        else:
            print('success to connect hentai')
    else:
        print('local cookies missing, you deleted it?')
        session = False

    return session