# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seating', '0008_auto_20160513_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seating',
            name='number_of_seats',
            field=models.IntegerField(default=0, help_text=b'This field is automatically updated to match the chosen layout. Change the chosen layout to alter this field', verbose_name=b'number of seats'),
            preserve_default=True,
        ),
    ]
