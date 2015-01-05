# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0005_auto_20150103_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sponsorrelation',
            options={'ordering': ['-priority']},
        ),
    ]
