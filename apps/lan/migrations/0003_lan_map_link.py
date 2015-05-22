# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0002_auto_20150107_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='lan',
            name='map_link',
            field=models.CharField(help_text=b'url for google maps embedded map', max_length=300, null=True, verbose_name=b'map link'),
            preserve_default=True,
        ),
    ]
