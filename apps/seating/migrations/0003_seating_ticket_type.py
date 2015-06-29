# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0002_auto_20150107_2031'),
        ('seating', '0002_auto_20150108_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='seating',
            name='ticket_type',
            field=models.ForeignKey(blank=True, to='lan.TicketType', null=True),
            preserve_default=True,
        ),
    ]
