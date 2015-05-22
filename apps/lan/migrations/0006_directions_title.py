# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0005_auto_20150522_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='directions',
            name='title',
            field=models.TextField(null=True, verbose_name=b'title'),
            preserve_default=True,
        ),
    ]
