# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competition', '0005_auto_20160205_1524'),
        ('userprofile', '0003_auto_20150108_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(max_length=20, verbose_name='nick')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AliasType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(help_text=b'Short description', max_length=100, verbose_name='nick')),
                ('profile_url', models.URLField(null=True, verbose_name=b'Challonge url', blank=True)),
                ('activity', models.ForeignKey(related_name='alias_type', to='competition.Activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='alias',
            name='alias_type',
            field=models.ForeignKey(to='userprofile.AliasType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alias',
            name='user',
            field=models.ForeignKey(related_name='alias', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='alias',
            unique_together=set([('user', 'alias_type')]),
        ),
    ]
