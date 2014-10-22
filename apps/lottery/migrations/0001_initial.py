# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lottery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('registration_open', models.BooleanField(default=False, verbose_name=b'Open')),
                ('multiple_winnings', models.BooleanField(default=False, help_text=b'Allows a user to win more than one price', verbose_name=b'Multiple winnings')),
                ('lan', models.ForeignKey(to='lan.LAN')),
            ],
            options={
                'verbose_name_plural': 'Lotteries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LotteryParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('has_won', models.BooleanField(default=False, verbose_name=b'has won')),
                ('lottery', models.ForeignKey(to='lottery.Lottery')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LotteryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=15, verbose_name='language', choices=[(b'nb', 'Norsk'), (b'en', 'English')])),
                ('title', models.CharField(max_length=50, verbose_name=b'title')),
                ('description', models.TextField(verbose_name=b'description')),
                ('model', models.ForeignKey(related_name='translations', verbose_name=b'lottery', to='lottery.Lottery')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LotteryWinner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lottery', models.ForeignKey(to='lottery.Lottery')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
