from django.http import HttpResponse
from django.shortcuts import render
from .task import add2,add
# Create your views here.


def add(request):
    res = add2.delay(3, 5)
    return HttpResponse('正在处理中...任务id：%s' % res.id)