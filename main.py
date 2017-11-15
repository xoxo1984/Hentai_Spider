# -*- coding: UTF-8 -*-

import codecs, os, copy, json
from concurrent.futures import ThreadPoolExecutor
from const import *
from config import get_args
from login_hentai import login_hentai
from build_session import build_session
from process_task_list import process_task_list
from collect_pic_url import collect_pic_page_url
from worker import download_pic


def analyze_url_and_gallery(url, session):
    print('analyzing ' + url)
    gallery_available, title, pic_page_url_list = collect_pic_page_url(url, session)
    if gallery_available:
        title_for_path = copy.deepcopy(title)
        illegal_str = [':', '\\', '/', '?', '|', '*']  # 替换非法字符
        for character in illegal_str:
            if title_for_path.find(character) != -1:
                title_for_path = title_for_path.replace(character, ' ')
        gallery_folder = os.path.join(args.savedir, title_for_path)
        if gallery_folder[-1] is ' ':
            gallery_folder = gallery_folder[:-1]

        page_num = len(pic_page_url_list)

        if '(' in url and ')' in url:
            page_from = int(url[url.find('(') + 1:url.rfind('-')])
            if '-' in url:
                page_end = int(url[url.find('-') + 1:url.rfind(')')])
            else:
                page_end = page_from  # exhentai会自动跳转到正确网址，所以不去删除括号
        else:
            page_from = 1
            page_end = page_num
        download_pic_page_url_list = pic_page_url_list[page_from - 1:page_end]
    else:
        print('something wrong with this gallery, please check')
        title = gallery_folder = page_num = page_from = page_end = download_pic_page_url_list = []
    print(title + ' ' + str(page_num) + ' pages')
    return title, gallery_folder, page_num, page_from, page_end, download_pic_page_url_list


def create_info_log(gallery_folder, title, url, page_num):
    info_path = os.path.join(gallery_folder, GALLERY_INFO_FILE)
    with codecs.open(info_path, 'w', 'utf-8') as f:
        f.write(title + '\r\n')
        f.write(url + '\r\n')
        f.write(str(page_num) + ' Pages' + '\r\n\r\n')
        f.write('Download by Hentai Spider' + '\r\n')


if __name__ == "__main__":

    program_folder = os.path.abspath(os.path.dirname(__file__))
    args = get_args(program_folder)

    if os.path.exists(LOCAL_COOKIES_FILE) is False:
        login_hentai(args.username, args.password)
    try:
        session = build_session()
    except:
        print('cannot build session')

    if session:
        if args.continuedownload:
            # load last_gallery_download_task and continue download
            try:
                with open(LAST_GALLERY_DOWNLOAD_TASK_FILE, 'r') as f:
                    last_gallery_download_task = json.loads(f.read())
            except:
                last_gallery_download_task = []
            if len(last_gallery_download_task) > 2:
                gallery_folder = last_gallery_download_task[0]
                title = last_gallery_download_task[1]
                download_pic_page_url_list = last_gallery_download_task[2:]
                if os.path.exists(gallery_folder) is False:
                    os.makedirs(gallery_folder)
                print('continue download unfinished task')
                with ThreadPoolExecutor(max_workers=args.thread) as executor:
                    for download_pic_page_url in download_pic_page_url_list:
                        try:
                            future = executor.submit(download_pic, download_pic_page_url, gallery_folder,
                                                     args.trynum, args.rename, args.oripic, args.log,
                                                     args.timeout, title, session)
                        except:
                            print('error occurs when downloading ' + download_pic_page_url)
                            if args.log is True:
                                fail_log_file = os.path.join(gallery_folder, FAIL_LOG_FILE)
                                with open(fail_log_file, 'a') as f:
                                    f.write(download_pic_page_url + '\r\n')
            os.remove(LAST_GALLERY_DOWNLOAD_TASK_FILE)

        try:
            with open(TASK_LIST_FILE, 'rb') as f:
                tasks_list = f.read()
                tasks_list = tasks_list.decode('utf-8')
        except:
            print('something wrong with ' + TASK_LIST_FILE)
        urls = process_task_list(tasks_list)

        print('task num: ' + str(len(urls)))
        for url in urls:
            title, gallery_folder, page_num, page_from, page_end, download_pic_page_url_list = analyze_url_and_gallery(
                url, session)
            if os.path.exists(gallery_folder) is False:
                os.makedirs(gallery_folder)
            if args.log:
                create_info_log(gallery_folder, title, url, page_num)

            # 保存任务信息以免程序被中断
            last_gallery_download_task = [gallery_folder, title] + download_pic_page_url_list
            with open(LAST_GALLERY_DOWNLOAD_TASK_FILE, 'w') as f:
                f.write(json.dumps(last_gallery_download_task))

            # 下载此gallery
            with ThreadPoolExecutor(max_workers=args.thread) as executor:
                for download_pic_page_url in download_pic_page_url_list:
                    try:
                        future = executor.submit(download_pic, download_pic_page_url, gallery_folder, args.trynum,
                                                 args.rename, args.oripic, args.log, args.timeout, title, session)
                    except:
                        print('error occurs when downloading ' + download_pic_page_url)
                        if args.log is True:  # 记录失败信息
                            fail_log_file = os.path.join(gallery_folder, FAIL_LOG_FILE)
                            with open(fail_log_file, 'a') as f:
                                f.write(download_pic_page_url + '\r\n')

            os.remove(LAST_GALLERY_DOWNLOAD_TASK_FILE)
