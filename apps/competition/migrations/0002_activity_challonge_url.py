# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='challonge_url',
            field=models.URLField(null=True, verbose_name=b'Challonge url', blank=True),
            preserve_default=True,
        ),
    ]
