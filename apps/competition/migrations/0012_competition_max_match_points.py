# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0011_auto_20170107_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='max_match_points',
            field=models.SmallIntegerField(default=1, help_text=b'This number represents how many points are needed to win a match. E.g. 3 in a BO 5 or 16 in BO 30', verbose_name=b'Maximum match points'),
            preserve_default=True,
        ),
    ]
