# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0004_auto_20150511_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='enforce_payment',
            field=models.BooleanField(default=False, help_text=b'If checked, teams will require x members (specified in team_size) with valid tickets before being able to sign up.', verbose_name=b'enforce payment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='competition',
            name='enforce_team_size',
            field=models.BooleanField(default=False, help_text=b'If checked, teams will require x members (specified in team_size) before being able to sign up.', verbose_name=b'enforce teams'),
            preserve_default=True,
        ),
    ]
