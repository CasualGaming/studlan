# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='banner',
            field=models.CharField(default=datetime.datetime(2014, 12, 26, 6, 19, 5, 778000), help_text=b'Use a mirrored image of at least a height of 150px.', max_length=100, verbose_name=b'Image url', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sponsor',
            name='description',
            field=models.TextField(default='test', verbose_name=b'description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sponsor',
            name='logo',
            field=models.CharField(default='irl', help_text=b'Use a mirrored image of at least a height of 150px.', max_length=100, verbose_name=b'Image url', blank=True),
            preserve_default=False,
        ),
    ]
