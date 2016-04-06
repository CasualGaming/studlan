# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20160209_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliastype',
            name='activity',
            field=models.ForeignKey(related_name='alias_type', to='competition.Activity', unique=True),
            preserve_default=True,
        ),
    ]
