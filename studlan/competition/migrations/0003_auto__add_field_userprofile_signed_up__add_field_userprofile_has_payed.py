# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'UserProfile.signed_up'
        db.add_column('competition_userprofile', 'signed_up', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'UserProfile.has_payed'
        db.add_column('competition_userprofile', 'has_payed', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'UserProfile.wants_to_sit_with'
        db.add_column('competition_userprofile', 'wants_to_sit_with', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'UserProfile.gender'
        db.add_column('competition_userprofile', 'gender', self.gf('django.db.models.fields.SmallIntegerField')(default=1), keep_default=False)

        # Adding field 'UserProfile.date_of_birth'
        db.add_column('competition_userprofile', 'date_of_birth', self.gf('django.db.models.fields.DateField')(default=datetime.date.today), keep_default=False)

        # Adding field 'UserProfile.address'
        db.add_column('competition_userprofile', 'address', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'UserProfile.zip_code'
        db.add_column('competition_userprofile', 'zip_code', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True), keep_default=False)

        # Adding field 'UserProfile.phone'
        db.add_column('competition_userprofile', 'phone', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'UserProfile.signed_up'
        db.delete_column('competition_userprofile', 'signed_up')

        # Deleting field 'UserProfile.has_payed'
        db.delete_column('competition_userprofile', 'has_payed')

        # Deleting field 'UserProfile.wants_to_sit_with'
        db.delete_column('competition_userprofile', 'wants_to_sit_with')

        # Deleting field 'UserProfile.gender'
        db.delete_column('competition_userprofile', 'gender')

        # Deleting field 'UserProfile.date_of_birth'
        db.delete_column('competition_userprofile', 'date_of_birth')

        # Deleting field 'UserProfile.address'
        db.delete_column('competition_userprofile', 'address')

        # Deleting field 'UserProfile.zip_code'
        db.delete_column('competition_userprofile', 'zip_code')

        # Deleting field 'UserProfile.phone'
        db.delete_column('competition_userprofile', 'phone')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'competition.activity': {
            'Meta': {'ordering': "['title']", 'object_name': 'Activity'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'competition.competition': {
            'Meta': {'ordering': "['status', 'title']", 'object_name': 'Competition'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Activity']"}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['competition.Team']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'use_teams': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'competition.team': {
            'Meta': {'ordering': "['tag', 'title']", 'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'team_members'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'competition.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'gender': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'has_payed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'signed_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'wants_to_sit_with': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['competition']
