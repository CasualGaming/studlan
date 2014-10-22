# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name=b'title')),
                ('image_url', models.CharField(help_text=b'Use a mirrored image of at least a height of 150px.', max_length=100, verbose_name=b'Image url', blank=True)),
                ('desc', models.TextField(verbose_name=b'description')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'activity',
                'verbose_name_plural': 'activities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.SmallIntegerField(verbose_name=b'status', choices=[(1, b'Open'), (2, b'Closed'), (3, b'In progress'), (4, b'Finished')])),
                ('use_teams', models.BooleanField(default=False, help_text=b'If checked, participants will be ignored, and will instead use teams. If left unchecked teams will be ignored, and participants will be used.', verbose_name=b'use teams')),
                ('activity', models.ForeignKey(to='competition.Activity')),
                ('lan', models.ForeignKey(to='lan.LAN')),
            ],
            options={
                'ordering': ['status'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompetitionTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=15, verbose_name='language', choices=[(b'nb', 'Norsk'), (b'en', 'English')])),
                ('translated_title', models.CharField(max_length=50, verbose_name=b'title')),
                ('translated_description', models.TextField(help_text=b'Markdown-enabled. You may also use regular (x)HTML markup. For blockquotes use the following markup:<br/><br/>&lt;blockquote&gt;<br/>&nbsp;&nbsp;&nbsp;&nbsp;&lt;p&gt;Quote-text& lt;/p&gt;<br/>&nbsp;&nbsp;&nbsp;&nbsp;&lt;small&gt;Reference&lt;/small&gt;<br/>&lt;/blockquote&gt;', verbose_name=b'description')),
                ('model', models.ForeignKey(related_name='translations', verbose_name=b'competition', to='competition.Competition')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competition', models.ForeignKey(to='competition.Competition')),
                ('team', models.ForeignKey(to='team.Team', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['user', 'team'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='participant',
            unique_together=set([('user', 'competition'), ('team', 'competition')]),
        ),
    ]
