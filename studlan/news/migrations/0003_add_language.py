# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for article in orm.Article.objects.all():
            at = orm.ArticleTranslation(article)
            at.language = 'nb'
            article.translated_title = article.title
            article.translated_body = article.body
            at.save()
            article.save()
            #article.translated_title = article.title
            #article.translated_body = article.body
            #article.model_id = article.id
            #article.language = 'nb'
            #article.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        'news.article': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'news.articletranslation': {
            'Meta': {'object_name': 'ArticleTranslation'},
            'translated_body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': "orm['news.Article']"}),
            'translated_title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['news']
    symmetrical = True
