# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0008_auto_20170106_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matchid', models.CharField(max_length=50, verbose_name=b'matchid')),
                ('p1_reg_score', models.CharField(max_length=50, null=True, verbose_name=b'p1_reg_score')),
                ('p2_reg_score', models.CharField(max_length=50, null=True, verbose_name=b'p2_reg_score')),
                ('final_score', models.CharField(max_length=50, null=True, verbose_name=b'final_score')),
                ('competition', models.ForeignKey(to='competition.Competition')),
                ('player1', models.ForeignKey(related_name='player1', to='competition.Participant', null=True)),
                ('player2', models.ForeignKey(related_name='player2', to='competition.Participant', null=True)),
                ('winner', models.ForeignKey(related_name='winner', to='competition.Participant', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
