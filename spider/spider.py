# coding: utf-8
from django.utils import timezone
import re
from datetime import datetime
import time
from dateutil import tz
from bs4 import BeautifulSoup
from spider.models import Article, Process
from spider.utils import get_tree, get

ARTICLE_LIST_URL = 'http://wallstreetcn.com/search?q={0}&page={1}'
ARTICLE_URL = 'http://wallstreetcn.com/node/{0}'


def parser_page(keyword, total_page=1):
    print('Starting fetch article:{0} total page:{1}'.format(keyword, total_page))
    start = time.time()

    for i in range(total_page):
        print('{0}资讯 第{1}页'.format(keyword, str(i + 1)))
        article_ids = paser_article_list(keyword, i + 1)

        for id in article_ids:
            parser_article(id, keyword)

    unprocess = Process.objects.filter(status=Process.PENDING)
    for p in unprocess:
        parser_article(p.id)

    print('Finished fetch article  Cost: {}'.format(time.time() - start))


def paser_article_list(keyword, page):
    url = ARTICLE_LIST_URL.format(keyword, str(page))
    tree = get_tree(url)

    articles = tree.xpath('//div[@class="post"]/a[@class="post__image"]/@href')
    pattern = re.compile('\S*?(?P<id>\d+)')

    article_ids = []
    for i in articles:
        m = pattern.match(i)
        id = m.group('id')
        article_ids.append(id)

    return article_ids


def parser_article(article_id, keyword=None):
    url = ARTICLE_URL.format(article_id)

    process, is_created = Process.objects.get_or_create(id=article_id)
    if process.is_success:
        return

    res = get(url)
    is_success = save_article(res, keyword)

    process.make_status(is_success)


def save_article(res, keyword):
    m = re.match('\S+?(\d+)', res.url)
    article_id = m.group(1)

    soup = BeautifulSoup(res.text, 'lxml')
    title = soup.find('div', class_='title-text')
    author = soup.find('a', class_='author-name')

    # soup.title.text='Page Not Found'

    try:
        if not author:
            author = soup.find('div', class_='title-meta-source')

        title = title.text.strip()
        author = author.text.strip()

        print(article_id)
        print(title)
        print(author)

        createtime = soup.find('div', class_='title-meta-time').contents[2].strip()
        createtime = datetime.strptime(createtime, '%Y年%m月%d日 %H:%M:%S')
        createtime=createtime.replace(tzinfo=tz.gettz('UTC'))
        content = soup.find('div', class_='page-article-content')

        article = {
            'title': title,
            'author': author,
            'content': str(content),
            'tag': keyword,
            'createtime': createtime
        }

        article, is_created = Article.objects.get_or_create(id=int(article_id), defaults=article)

        return True
    except Exception as e:
        print('fetch article {0} error：{1}'.format(article_id, e))
        return False
