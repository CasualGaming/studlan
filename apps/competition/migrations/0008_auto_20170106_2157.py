# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0007_participant_cid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='cid',
            field=models.CharField(max_length=50, null=True, verbose_name=b'cid'),
            preserve_default=True,
        ),
    ]
