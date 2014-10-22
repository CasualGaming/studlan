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
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name=b'date joined')),
            ],
            options={
                'ordering': ['user'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name=b'title')),
                ('tag', models.CharField(unique=True, max_length=10, verbose_name=b'tag')),
                ('leader', models.ForeignKey(related_name='newteamleader', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='new_team_members', through='team.Member', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['tag', 'title'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(to='team.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set([('team', 'user')]),
        ),
    ]
