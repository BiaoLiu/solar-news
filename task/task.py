# coding:utf-8
from celery import task
# from task.celery import app



@task(name='相加的task')
def add(x, y):
    return x + y


@task(name='相加的task2')
def add2(x, y):
    return x + y
