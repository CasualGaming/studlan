# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('has_paid', models.BooleanField(default=False, verbose_name=b'has paid')),
                ('arrived', models.BooleanField(default=False, verbose_name=b'has arrived')),
            ],
            options={
                'ordering': ['-user', 'lan'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LAN',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'title')),
                ('start_date', models.DateTimeField(verbose_name=b'start date')),
                ('end_date', models.DateTimeField(verbose_name=b'end date')),
                ('location', models.CharField(max_length=100, verbose_name=b'location')),
                ('description', models.TextField(verbose_name=b'description')),
            ],
            options={
                'ordering': ['start_date'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='attendee',
            name='lan',
            field=models.ForeignKey(to='lan.LAN'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendee',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
