# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Sponsor.website'
        db.alter_column('sponsor_sponsor', 'website', self.gf('django.db.models.fields.URLField')(max_length=200))


    def backwards(self, orm):
        
        # Changing field 'Sponsor.website'
        db.alter_column('sponsor_sponsor', 'website', self.gf('django.db.models.fields.CharField')(max_length=200))


    models = {
        'sponsor.sponsor': {
            'Meta': {'ordering': "['priority']", 'object_name': 'Sponsor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['sponsor']
