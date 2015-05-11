# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_auto_20150108_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='enforce_payment',
            field=models.BooleanField(default=False, help_text=b'If checked, teams will require 5 members with valid tickets before being able to sign up.', verbose_name=b'enforce payment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competition',
            name='enforce_team_size',
            field=models.BooleanField(default=False, help_text=b'If checked, teams will require 5 members before being able to sign up.', verbose_name=b'enforce teams'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competition',
            name='team_size',
            field=models.IntegerField(default=5, blank=True),
            preserve_default=True,
        ),
    ]
