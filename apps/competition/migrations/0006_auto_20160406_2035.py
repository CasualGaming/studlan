# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0005_auto_20160205_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='require_alias',
            field=models.BooleanField(default=False, help_text=b'If checked, players will need to registeran alias for the Activity that the competition belongs to.', verbose_name=b'require alias'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competition',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
