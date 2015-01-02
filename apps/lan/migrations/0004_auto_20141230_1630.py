# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0003_auto_20141227_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='LANTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=15, verbose_name='language', choices=[(b'nb', 'Norsk'), (b'en', 'English')])),
                ('description', models.TextField(verbose_name=b'description')),
                ('model', models.ForeignKey(related_name='translations', verbose_name=b'LAN', to='lan.LAN')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='lan',
            name='description',
        ),
    ]
