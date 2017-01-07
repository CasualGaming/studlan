# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_auto_20170106_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 7, 12, 49, 57, 350489), verbose_name=b'created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
