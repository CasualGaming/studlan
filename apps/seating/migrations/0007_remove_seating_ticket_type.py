# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seating', '0006_seating_ticket_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seating',
            name='ticket_type',
        ),
    ]
