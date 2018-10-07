# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-07 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20181007_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
            name='relevant_to',
        ),
        migrations.RemoveField(
            model_name='toparents',
            name='relevant_to',
        ),
        migrations.AddField(
            model_name='faq',
            name='active',
            field=models.BooleanField(default=False, verbose_name=b'isActive'),
        ),
        migrations.AddField(
            model_name='toparents',
            name='active',
            field=models.BooleanField(default=False, verbose_name=b'isActive'),
        ),
    ]
