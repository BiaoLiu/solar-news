# coding: utf-8
from datetime import datetime
import time
from queue import Queue

from spider.models import Article
from spider.utils import get_tree, get_html, get
import re
import threading

ARTICLE_LIST_URL = 'http://wallstreetcn.com/search?q={0}&page={1}'

ARTICLE_URL = 'http://wallstreetcn.com/node/{0}'

article_queue = Queue()
html_queue = Queue()


def paser_article_list(keyword, page):
    url = ARTICLE_LIST_URL.format(keyword, str(page))
    tree = get_tree(url)

    articles = tree.xpath('//div[@class="post"]/a[@class="post__image"]/@href')

    pattern = re.compile('\w*?(?P<id>\d+)')

    for i in articles:
        m = pattern.match(i)
        id = m.group('id')

        article_queue.put(id)
        print(id)
        # print(i.attrib.get('href'))

    parser_article(id)

    article_queue.qsize()
    article_queue.get()


# def paser_article(article_id):
#     url = ARTICLE_URL.format(article_id)
#     tree = get_tree(url)
#
#     title = tree.xpath('//div[@class="title-text"]/text()')[0]
#     createtime = tree.xpath('//div[@class="title-meta-time"]/text()')[1].rstrip()
#
#     print(title)
#     createtime = datetime.strptime(str(createtime), '%Y年%m月%d日 %H:%M:%S')
#     print(createtime)
#
#     p = tree.xpath('//div[@class="page-article-content"]//p/node()')
#
#     for i in p:
#         # print(i)
#         # if issubclass(i)
#         if isinstance(i,_Element):
#             info = i.xpath('string(.)')
#             print(info)

class Downloader(threading.Thread):
    def run(self):
        global article_queue
        while True:
            if article_queue.qsize() > 0:
                article_id = article_queue.get()
                print('抓取文章:' + article_id)
                url = ARTICLE_URL.format(article_id)
                result = get(url)
                html_queue.put(result.text)
            time.sleep(60 * 1)


class ItemPipline(threading.Thread):
    def run(self):
        title = soup.find('div', class_='title-text')
        print(title.text)

        createtime = soup.find('div', class_='title-meta-time').contents[2].strip()

        # for i in createtime.contents:
        #     print(i)

        createtime = datetime.strptime(createtime, '%Y年%m月%d日 %H:%M:%S')

        div = soup.find('div', class_='page-article-content')

        print(div)

        article, is_created = Article.objects.get_or_create(id=int(article_id),
                                                            defaults={'title': title.text,
                                                                      'content': str(div),
                                                                      'createtime': createtime
                                                                      })


def parser_article(article_id):
    url = ARTICLE_URL.format(article_id)
    soup = get_html(url)
    title = soup.find('div', class_='title-text')
    print(title.text)

    createtime = soup.find('div', class_='title-meta-time').contents[2].strip()

    # for i in createtime.contents:
    #     print(i)

    createtime = datetime.strptime(createtime, '%Y年%m月%d日 %H:%M:%S')

    div = soup.find('div', class_='page-article-content')

    print(div)

    article, is_created = Article.objects.get_or_create(id=int(article_id),
                                                        defaults={'title': title.text,
                                                                  'content': str(div),
                                                                  'createtime': createtime
                                                                  })
