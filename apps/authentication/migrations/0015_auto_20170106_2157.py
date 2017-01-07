# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_auto_20170106_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 6, 21, 57, 26, 750989), verbose_name=b'created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
