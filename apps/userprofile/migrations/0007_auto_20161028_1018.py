# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_auto_20160406_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alias',
            name='nick',
            field=models.CharField(max_length=40, verbose_name=b'nick'),
            preserve_default=True,
        ),
    ]
