# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20150609_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 5, 15, 24, 23, 587829), verbose_name=b'created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
