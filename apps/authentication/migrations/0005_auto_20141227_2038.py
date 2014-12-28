# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20141227_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 27, 20, 38, 29, 317255), verbose_name=b'created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
