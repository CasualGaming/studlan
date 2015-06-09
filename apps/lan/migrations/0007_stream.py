# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0006_directions_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'title')),
                ('description', models.TextField(help_text=b'Short description that will show on front page.', verbose_name=b'description')),
                ('link', models.TextField(help_text=b'Embedding link for twitch etc. Include the complete IFrame.', verbose_name=b'link')),
                ('active', models.BooleanField(default=False, help_text=b'No more than one stream can be active at any given time.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
