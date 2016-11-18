# coding: utf-8
import random
import threading
from datetime import datetime
import time
from queue import Queue
from bs4 import BeautifulSoup
import re
from spider.models import Article
from spider.utils import get_tree, get_html, get

ARTICLE_LIST_URL = 'http://wallstreetcn.com/search?q={0}&page={1}'
ARTICLE_URL = 'http://wallstreetcn.com/node/{0}'

article_queue = Queue()
html_queue = Queue()


def parser_page(keyword, total_page=1):
    vm_page = WorkManager(1)
    for i in range(total_page):
        vm_page.add_job(paser_article_list, keyword, i + 1)

    vm_page.start()
    vm_page.wait_for_complete()

    vm_article = WorkManager(1)
    while vm_page.result_queue.qsize() > 0:
        article_ids = vm_page.result_queue.get()
        for id in article_ids:
            vm_article.add_job(parser_article, id)

    vm_article.start()
    vm_article.wait_for_complete()

    vm_save = WorkManager(1)
    vm_save.add_job(save_article, vm_article.result_queue)

    vm_save.start()
    vm_save.wait_for_complete()


def paser_article_list(keyword, page):
    print('正在执行')
    url = ARTICLE_LIST_URL.format(keyword, str(page))
    tree = get_tree(url)

    articles = tree.xpath('//div[@class="post"]/a[@class="post__image"]/@href')
    pattern = re.compile('\w*?(?P<id>\d+)')

    article_ids = []
    for i in articles:
        m = pattern.match(i)
        id = m.group('id')
        article_ids.append(id)
        print('article_id' + id)

    return article_ids


def parser_article(self, article_id):
    url = ARTICLE_URL.format(article_id)
    result = get(url)
    return result


def save_article(queue):
    if queue.qsize() > 0:
        result = queue.get()
        m = re.match('\S+(\d+)', result.url)
        article_id = m.group(1)
        soup = BeautifulSoup(result.text, 'lxml')
        title = soup.find('div', class_='title-text')
        author = soup.find('a', class_='author-name')

        print(title.text)
        print(author.text)

        createtime = soup.find('div', class_='title-meta-time').contents[2].strip()
        createtime = datetime.strptime(createtime, '%Y年%m月%d日 %H:%M:%S')
        content = soup.find('div', class_='page-article-content')
        print(content)

        article = {'title': title.text,
                   'author': author.text,
                   'content': str(content),
                   'createtime': createtime
                   }

        article, is_created = Article.objects.get_or_create(id=int(article_id), defaults=article)


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


class Worker(threading.Thread):
    def __init__(self, work_queue, result_queue):
        super(Worker, self).__init__()
        self.setDaemon(True)
        self.work_queue = work_queue
        self.result_queue = result_queue

    def run(self):
        while 1:
            try:
                print('线程{0}：正在执行'.format(threading.current_thread()))
                callable, args, kwargs = self.work_queue.get()
                result = callable(*args, **kwargs)
                print('线程：%s 执行结果：%s' % (threading.current_thread(), result))
                self.result_queue.put(result)
            except:
                break


class WorkManager:
    def __init__(self, num_of_workers):
        self.work_queue = Queue()
        self.result_queue = Queue()
        self.workers = []
        self._recruit_threads(num_of_workers)

    def _recruit_threads(self, num_of_workers):
        for _ in range(num_of_workers):
            worker = Worker(self.work_queue, self.result_queue)
            self.workers.append(worker)

    def add_job(self, callable, *args, **kwargs):
        self.work_queue.put((callable, args, kwargs))

    def start(self):
        for worker in self.workers:
            worker.start()
        print('All jobs were start.')

    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()
            if worker.isAlive and not self.work_queue.empty():
                self.workers.append(worker)
        print('All jobs were complete.')


def download(url):
    return random.randint(10)


if __name__ == '__main__':
    wm = WorkManager(10)
    urls = [x for x in range(10)]

    for url in urls:
        wm.add_job(download, url)

    wm.start()
    wm.wait_for_complete()
