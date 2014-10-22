# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(help_text=b'Specify a nick name (display name).', max_length=20, verbose_name=b'nick')),
                ('wants_to_sit_with', models.TextField(help_text=b'Names/nicks of people this user wants to sit with.', verbose_name=b'Wants to sit with', blank=True)),
                ('gender', models.SmallIntegerField(default=1, verbose_name=b'Gender', choices=[(1, b'Male'), (2, b'Female')])),
                ('date_of_birth', models.DateField(default=datetime.date.today, verbose_name=b'Date of birth')),
                ('address', models.CharField(max_length=100, verbose_name=b'Street address')),
                ('zip_code', models.CharField(max_length=4, verbose_name=b'Zip code')),
                ('phone', models.CharField(max_length=20, verbose_name=b'Phone number')),
                ('ntnu_username', models.CharField(max_length=20, null=True, verbose_name=b'NTNU username', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
