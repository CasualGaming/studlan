# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Article.body'
        db.delete_column('news_article', 'body')

        # Deleting field 'Article.title'
        db.delete_column('news_article', 'title')


    def backwards(self, orm):
        # Adding field 'Article.body'
        db.add_column('news_article', 'body',
                      self.gf('django.db.models.fields.TextField')(default='body'),
                      keep_default=False)

        # Adding field 'Article.title'
        db.add_column('news_article', 'title',
                      self.gf('django.db.models.fields.CharField')(default='title', max_length=50),
                      keep_default=False)


    models = {
        'news.article': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Article'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'news.articletranslation': {
            'Meta': {'object_name': 'ArticleTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': "orm['news.Article']"}),
            'translated_body': ('django.db.models.fields.TextField', [], {}),
            'translated_title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['news']