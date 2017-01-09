# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0012_competition_max_match_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='tournament_format',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Tournament format', choices=[(b'single elimination', b'Single elimination'), (b'double elimination', b'Double elimination')]),
            preserve_default=True,
        ),
    ]
