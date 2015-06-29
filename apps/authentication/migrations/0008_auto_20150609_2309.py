# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20150606_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 9, 23, 9, 27, 750003), verbose_name=b'created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
