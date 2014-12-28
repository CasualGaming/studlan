# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0002_auto_20141227_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickettype',
            name='description',
            field=models.TextField(null=True, verbose_name=b'Description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tickettype',
            name='title',
            field=models.CharField(default='Temp', max_length=50, verbose_name=b'Title'),
            preserve_default=False,
        ),
    ]
