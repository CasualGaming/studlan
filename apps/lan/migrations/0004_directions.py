# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0003_lan_map_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Directions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(verbose_name=b'directions')),
                ('lan', models.ForeignKey(to='lan.LAN')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
