import re
from bs4 import BeautifulSoup


def scrap_pic_page_url(url, session, all_pic_page_url_list):
    r = session.get(url=url)
    page_content = r.content.decode("utf-8")
    soup = BeautifulSoup(page_content, 'lxml')

    for item in soup.select('div#gdt a'):
        pic_url = item.get('href')
        all_pic_page_url_list.append(pic_url)

    for item in soup.select('td.ptds'):
        next = item.next_sibling
        if next.get('class') == ['ptdd']:
            next_page_url = False
        else:
            next_page_url = next.find('a').get('href')
    return next_page_url


def collect_pic_page_url(url, session):
    all_pic_page_url_list = []
    r = session.get(url=url)
    page_content = r.content.decode("utf-8")

    if r.status_code != 200 or 'Key missing' in page_content:
        gallery_available = False
        title = ''
    else:
        gallery_available = True
        if page_content.find('<h1 id="gj"></h1>') == -1:  # 优先用第二个title
            title = re.search('<h1 id="gj">+(.*?)+</h1>', page_content).group()[12:-5]
        else:
            title = re.search('<h1 id="gn">+(.*?)+</h1>', page_content).group()[12:-5]

        # first page
        next_page_url = scrap_pic_page_url(url, session, all_pic_page_url_list)
        # go on if can
        while next_page_url:
            next_page_url = scrap_pic_page_url(next_page_url, session, all_pic_page_url_list)

    return gallery_available, title, all_pic_page_url_list


if __name__ == '__main__':
    pass
