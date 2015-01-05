# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lan', '0005_auto_20141230_1757'),
        ('sponsor', '0003_auto_20141227_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lan', models.ForeignKey(to='lan.LAN')),
                ('sponsor', models.ForeignKey(to='sponsor.Sponsor')),
            ],
            options={
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
        migrations.RenameField(
            model_name='sponsor',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='description',
        ),
    ]
