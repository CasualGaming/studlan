# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seating', '0007_remove_seating_ticket_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seating',
            name='ticket_types',
            field=models.ManyToManyField(related_name='ticket_types', null=True, to='lan.TicketType', blank=True),
            preserve_default=True,
        ),
    ]
