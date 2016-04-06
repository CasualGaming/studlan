# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_auto_20160209_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliastype',
            name='description',
            field=models.CharField(help_text=b'Short description', max_length=100, verbose_name=b'Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aliastype',
            name='profile_url',
            field=models.URLField(help_text=b'Url where profile info can be retrieved. E.g. https://steamcommunity.com/id/', null=True, verbose_name=b'Profile url', blank=True),
            preserve_default=True,
        ),
    ]
