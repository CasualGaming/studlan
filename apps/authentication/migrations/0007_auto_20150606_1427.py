# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20150108_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 6, 14, 27, 30, 704589), verbose_name=b'created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
