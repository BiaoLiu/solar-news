# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-17 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='createtime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='process',
            name='createtime',
            field=models.DateTimeField(),
        ),
    ]
