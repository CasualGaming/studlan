# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-08-04 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seating', '0013_auto_20200909_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='seating',
            name='priority',
            field=models.IntegerField(default=0, help_text='For ordering of seatings, higher number will show first.', verbose_name='priority'),
        ),
    ]