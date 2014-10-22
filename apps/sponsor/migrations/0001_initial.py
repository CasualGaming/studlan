# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'name')),
                ('website', models.URLField(verbose_name=b'website')),
                ('priority', models.IntegerField(help_text=b'higher priority means closer to the top of the sponsor list.', verbose_name=b'priority')),
            ],
            options={
                'ordering': ['priority'],
            },
            bases=(models.Model,),
        ),
    ]
