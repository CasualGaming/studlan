# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lan', '0001_initial'),
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
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bought_date', models.DateField()),
                ('valid', models.BooleanField(default=True)),
                ('invalid_date', models.DateField(null=True, blank=True)),
                ('invalid_description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField(default=50, verbose_name=b'Price')),
                ('number_of_seats', models.IntegerField(verbose_name=b'Seats')),
                ('lan', models.ForeignKey(to='lan.LAN')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
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
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(to='lan.TicketType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='lan',
            name='description',
        ),
    ]
