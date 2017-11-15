# -*- coding: UTF-8 -*-

import re, os, time, json
from requests.exceptions import Timeout, ConnectionError
from const import *


def download_pic(download_pic_page_url, gallery_folder, trynum, rename, oripic, log, timeout, title, session):
    now_page = download_pic_page_url[download_pic_page_url.rfind('-') + 1:]
    print(now_page + ' start')
    start_time = time.time()

    try:
        # 收集pic_page_url上信息
        r = session.get(download_pic_page_url)
        page_content = r.content.decode('utf-8')
        pic_url = re.search('<img id="img" src="+(.*?)+"', page_content).group()[19:-1]
        temp = re.findall('/s/(.+?)"', page_content).pop()
        pagenum = temp[temp.rfind('-') + 1:]

        # 生成图片保存路径
        if rename is False:
            filename = pic_url[pic_url.rfind('/') + 1:]
            pic_path = os.path.join(gallery_folder, filename)
        elif rename is True:
            filename_postfix = pic_url[pic_url.rfind('.'):]
            # 由于图片的文件名的前缀位数不同，可能导致浏览顺序出错，所以添加逻辑，让文件名的前缀长度一致
            if len(str(pagenum)) == len(str(now_page)):
                filename_prefix = str(now_page)
            else:
                filename_prefix = (len(str(pagenum)) - len(str(now_page))) * '0' + str(now_page)
            filename = filename_prefix + filename_postfix
            pic_path = os.path.join(gallery_folder, filename)
        while os.path.exists(pic_path) is True:  # 当下载目录有一样的文件名的文件，则在原文件名前缀中添加一些字样，直到文件名不重复为止
            pic_path = pic_path[:-4] + '_2' + pic_path[-4:]  # 默认后缀名是3位

        # 提取原图的下载链接
        if oripic is True:
            if 'https://exhentai.org/fullimg' in page_content:  # 也要记录图片大小
                oripic_url = re.search('https://exhentai.org/fullimg.php(.*?)\"', page_content).group()[:-1].replace(
                    '&amp;', '&')
            else:  # 当没有原图时，则修改相应参数
                oripic = False
                oripic_url = pic_url
    except:
        pass

    # 下载图片
    tried = 1
    retry = 0
    fail_flag = True
    while retry <= trynum:
        try:
            if oripic:  # 原图
                r = session.get(oripic_url, timeout=timeout)
                pic_size = r.headers['Content-Length']  # 注意 pic_size是str类型
                if pic_size == str(len(r.content)):  # 判断下载是否成功
                    with open(pic_path, 'wb') as f:
                        f.write(r.content)
                    fail_flag = False
                    retry = trynum + 1
                else:
                    fail_flag = True
                    tried += 1
                    retry += 1
            else:  # 非原图
                r = session.get(pic_url, timeout=timeout)
                pic_size = r.headers['Content-Length']  # 注意 pic_size是str类型
                if pic_size == str(len(r.content)):  # 判断下载是否成功
                    with open(pic_path, 'wb') as f:
                        f.write(r.content)
                    fail_flag = False
                    retry = trynum + 1
                else:
                    fail_flag = True
                    tried += 1
                    retry += 1
        except:
        # except (Timeout, ConnectionError):
            fail_flag = True
            retry += 1
            tried += 1

    if fail_flag:
        if log:
            log_path = os.path.join(gallery_folder, FAIL_LOG_FILE)
            with open(log_path, 'a') as f:
                f.write(download_pic_page_url + '\r\n')
        spend_time = round(time.time() - start_time, 1)
        print(now_page + ' failed, tried ' + str(tried) + ', used time: ' + str(spend_time))
    else:
        with open(LAST_GALLERY_DOWNLOAD_TASK_FILE, "r") as f:
            last_gallery_download_task = json.loads(f.read())
            last_gallery_download_task.remove(download_pic_page_url)
        with open(LAST_GALLERY_DOWNLOAD_TASK_FILE, "w") as f:
            f.write(json.dumps(last_gallery_download_task))
        spend_time = round(time.time() - start_time, 1)
        print(str(now_page) + ' done, tried ' + str(tried) + ', used time: ' + str(spend_time))
