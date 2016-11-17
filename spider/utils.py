# coding: utf-8
from lxml import etree
import random
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from django.conf import settings

TIMEOUT = 5


def choice_proxy():
    if settings.PROXIES:
        return random.choice(settings.PROXIES)
    return ''


def get_user_agent():
    ua = UserAgent()
    return ua.random


def get(url, retry=0):
    s = requests.Session()
    proxies = {
        'http': choice_proxy()
    }
    s.headers.update({'user-agent': get_user_agent(),
                      'referer': 'http://wallstreetcn.com/'})

    try:
        result = s.get(url, timeout=TIMEOUT, proxies=proxies)
        result.encoding = 'utf-8'
        return result
    except requests.RequestException:
        if retry < 3:
            return get(url, retry=retry + 1)
        raise


def post(url):
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://wallstreetcn.com/'
    }

    return requests.post(url, headers=headers)


def get_tree(url):
    result = get(url)
    return etree.HTML(result.text)


def get_html(url):
    result = get(url)
    soup = BeautifulSoup(result.text, 'lxml')
    return soup
