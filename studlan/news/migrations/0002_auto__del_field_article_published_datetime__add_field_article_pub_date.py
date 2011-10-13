# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Article.published_datetime'
        db.delete_column('news_article', 'published_datetime')

        # Adding field 'Article.pub_date'
        db.add_column('news_article', 'pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Article.published_datetime'
        db.add_column('news_article', 'published_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)

        # Deleting field 'Article.pub_date'
        db.delete_column('news_article', 'pub_date')


    models = {
        'news.article': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['news']
