# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0004_directions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directions',
            name='description',
            field=models.TextField(null=True, verbose_name=b'directions'),
            preserve_default=True,
        ),
    ]
