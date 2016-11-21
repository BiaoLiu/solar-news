from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from spider.spider import parser_page


def spider_wallstreet(request):
    # for keyword in ['太阳能', '光伏', '晶硅', '多晶硅', '硅片']:
    #     parser_page(keyword, 2)


    parser_page('太阳能', 1)

    return HttpResponse('success')
