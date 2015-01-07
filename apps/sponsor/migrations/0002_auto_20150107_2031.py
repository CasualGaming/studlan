# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0002_auto_20150107_2031'),
        ('sponsor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.IntegerField(help_text=b'higher priority means closer to the top of the sponsor list.', verbose_name=b'priority')),
                ('lan', models.ForeignKey(to='lan.LAN')),
                ('sponsor', models.ForeignKey(to='sponsor.Sponsor')),
            ],
            options={
                'ordering': ['-priority'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SponsorTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=15, verbose_name='language', choices=[(b'nb', 'Norsk'), (b'en', 'English')])),
                ('description', models.TextField(verbose_name=b'description')),
                ('model', models.ForeignKey(related_name='translations', verbose_name=b'Sponsor', to='sponsor.Sponsor')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='sponsor',
            options={},
        ),
        migrations.RenameField(
            model_name='sponsor',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='priority',
        ),
        migrations.AddField(
            model_name='sponsor',
            name='banner',
            field=models.CharField(default='', help_text=b'Use a mirrored image of at least a height of 150px.', max_length=100, verbose_name=b'Banner url', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sponsor',
            name='logo',
            field=models.CharField(default='', help_text=b'Use a mirrored image of at least a height of 150px.', max_length=100, verbose_name=b'Logo url', blank=True),
            preserve_default=False,
        ),
    ]
