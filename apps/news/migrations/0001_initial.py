# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'published')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=15, verbose_name='language', choices=[(b'nb', 'Norsk'), (b'en', 'English')])),
                ('translated_title', models.CharField(max_length=50, verbose_name=b'title')),
                ('translated_body', models.TextField(verbose_name=b'body')),
                ('model', models.ForeignKey(related_name='translations', verbose_name=b'Article', to='news.Article')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
