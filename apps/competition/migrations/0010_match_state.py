# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0009_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='state',
            field=models.CharField(default='pending', max_length=50, verbose_name=b'state'),
            preserve_default=False,
        ),
    ]
