# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0002_auto_20150107_2031'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('placement', models.IntegerField(verbose_name=b'placement id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name=b'title')),
                ('desc', models.CharField(max_length=250, verbose_name=b'desc')),
                ('number_of_seats', models.IntegerField(verbose_name=b'number of seats')),
                ('closing_date', models.DateTimeField(verbose_name=b'closing date')),
                ('template', models.TextField(null=True, verbose_name=b'SVG layout for seating', blank=True)),
                ('lan', models.ForeignKey(to='lan.LAN')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='seat',
            name='seating',
            field=models.ForeignKey(to='seating.Seating'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seat',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
