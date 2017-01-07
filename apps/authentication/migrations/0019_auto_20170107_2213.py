# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_auto_20170107_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 7, 22, 13, 58, 323019), verbose_name=b'created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
