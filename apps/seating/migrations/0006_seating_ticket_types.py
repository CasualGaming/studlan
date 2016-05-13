# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0008_auto_20160205_1537'),
        ('seating', '0005_auto_20150609_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='seating',
            name='ticket_types',
            field=models.ManyToManyField(related_name='ticket_types', to='lan.TicketType'),
            preserve_default=True,
        ),
    ]
