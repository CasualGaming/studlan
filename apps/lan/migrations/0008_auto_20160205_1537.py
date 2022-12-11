# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0007_stream'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendee',
            unique_together=set([('user', 'lan')]),
        ),
    ]
