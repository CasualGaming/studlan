# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0004_auto_20141230_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketTypeTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=15, verbose_name='language', choices=[(b'nb', 'Norsk'), (b'en', 'English')])),
                ('title', models.CharField(max_length=50, verbose_name=b'Title')),
                ('description', models.TextField(null=True, verbose_name=b'Description', blank=True)),
                ('model', models.ForeignKey(related_name='translations', verbose_name=b'TicketType', to='lan.TicketType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='tickettype',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tickettype',
            name='title',
        ),
    ]
