# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seating', '0004_auto_20150510_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layout',
            name='description',
            field=models.CharField(max_length=250, verbose_name=b'description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='seating',
            name='desc',
            field=models.CharField(max_length=250, verbose_name=b'description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='seating',
            name='layout',
            field=models.ForeignKey(default=1, to='seating.Layout'),
            preserve_default=False,
        ),
    ]
