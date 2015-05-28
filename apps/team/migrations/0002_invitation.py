# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(verbose_name=b'token', max_length=32, editable=False)),
                ('invitee', models.ForeignKey(related_name='Invitee', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(to='team.Team')),
                ('team_leader', models.ForeignKey(related_name='Team Leader', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
