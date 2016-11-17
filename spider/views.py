from django.http import HttpResponse
from django.shortcuts import render
from .spider import paser_article_list
# Create your views here.

def test(request):
    paser_article_list('太阳能', 1)

    return HttpResponse('success')