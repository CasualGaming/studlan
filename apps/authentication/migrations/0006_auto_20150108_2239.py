# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20150108_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 8, 22, 39, 35, 257414), verbose_name=b'created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
