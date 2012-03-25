# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Sponsor'
        db.create_table('sponsor_sponsor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('priority', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('sponsor', ['Sponsor'])


    def backwards(self, orm):
        
        # Deleting model 'Sponsor'
        db.delete_table('sponsor_sponsor')


    models = {
        'sponsor.sponsor': {
            'Meta': {'ordering': "['priority']", 'object_name': 'Sponsor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['sponsor']
