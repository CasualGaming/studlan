# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_auto_20160209_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 12, 12, 12, 56, 848487), verbose_name=b'created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
