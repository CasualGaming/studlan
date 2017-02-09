# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0006_auto_20160406_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='cid',
            field=models.CharField(max_length=50, null=True, verbose_name=b'title'),
            preserve_default=True,
        ),
    ]
