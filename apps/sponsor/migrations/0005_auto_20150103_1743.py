# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0004_auto_20150103_1644'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sponsor',
            options={},
        ),
        migrations.AlterModelOptions(
            name='sponsorrelation',
            options={'ordering': ['priority']},
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='priority',
        ),
        migrations.AddField(
            model_name='sponsorrelation',
            name='priority',
            field=models.IntegerField(default=1, help_text=b'higher priority means closer to the top of the sponsor list.', verbose_name=b'priority'),
            preserve_default=False,
        ),
    ]
