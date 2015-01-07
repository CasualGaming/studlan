# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20141031_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 7, 20, 30, 56, 93009), verbose_name=b'created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
