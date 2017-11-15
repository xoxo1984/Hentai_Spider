import re


def process_task_list(raw_url):
    # 去空格
    urls = raw_url.replace(' ', '')
    # 分割
    urls = re.split('\r|\n|\r\n|,', urls)
    # 去重
    urls_temp = urls
    urls = list(set(urls_temp))
    urls.sort(key=urls_temp.index)
    # 删除多余空行导致的错误任务
    if '' in urls:
        urls.remove('')

    return urls
