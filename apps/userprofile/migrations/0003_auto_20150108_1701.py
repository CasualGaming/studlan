# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20141031_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.SmallIntegerField(default=1, blank=True, verbose_name='Gender', choices=[(1, 'Male'), (2, 'Female')]),
            preserve_default=True,
        ),
    ]
