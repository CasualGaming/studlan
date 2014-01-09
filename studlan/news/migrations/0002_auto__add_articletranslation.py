# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArticleTranslation'
        db.create_table('news_articletranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('translated_model', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['news.Article'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('translated_body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('news', ['ArticleTranslation'])


    def backwards(self, orm):
        # Deleting model 'ArticleTranslation'
        db.delete_table('news_articletranslation')


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
