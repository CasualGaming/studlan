# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seating', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name=b'title')),
                ('description', models.CharField(max_length=250, verbose_name=b'desc')),
                ('number_of_seats', models.IntegerField(verbose_name=b'number of seats')),
                ('template', models.TextField(null=True, verbose_name=b'SVG layout for seating', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='seating',
            name='template',
        ),
        migrations.AddField(
            model_name='seating',
            name='layout',
            field=models.ForeignKey(blank=True, to='seating.Layout', null=True),
            preserve_default=True,
        ),
    ]
