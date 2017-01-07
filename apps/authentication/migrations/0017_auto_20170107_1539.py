# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_auto_20170107_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 7, 15, 38, 51, 42575), verbose_name=b'created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
