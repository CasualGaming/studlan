# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0002_auto_20141226_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='banner',
            field=models.CharField(help_text=b'Use a mirrored image of at least a height of 150px.', max_length=100, verbose_name=b'Banner url', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='logo',
            field=models.CharField(help_text=b'Use a mirrored image of at least a height of 150px.', max_length=100, verbose_name=b'Logo url', blank=True),
            preserve_default=True,
        ),
    ]
