# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Participant'
        db.create_table('competition_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['team.Team'], null=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competition.Competition'])),
        ))
        db.send_create_signal('competition', ['Participant'])

        # Adding unique constraint on 'Participant', fields ['user', 'competition']
        db.create_unique('competition_participant', ['user_id', 'competition_id'])

        # Adding unique constraint on 'Participant', fields ['team', 'competition']
        db.create_unique('competition_participant', ['team_id', 'competition_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Participant', fields ['team', 'competition']
        db.delete_unique('competition_participant', ['team_id', 'competition_id'])

        # Removing unique constraint on 'Participant', fields ['user', 'competition']
        db.delete_unique('competition_participant', ['user_id', 'competition_id'])

        # Deleting model 'Participant'
        db.delete_table('competition_participant')


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
        'competition.participant': {
            'Meta': {'unique_together': "(('user', 'competition'), ('team', 'competition'))", 'object_name': 'Participant'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['competition.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team.Team']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'competition.team': {
            'Meta': {'ordering': "['tag', 'title']", 'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'team_members'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'team.member': {
            'Meta': {'ordering': "['user']", 'unique_together': "(('team', 'user'),)", 'object_name': 'Member'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['team.Team']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'team.team': {
            'Meta': {'ordering': "['tag', 'title']", 'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newteamleader'", 'to': "orm['auth.User']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'new_team_members'", 'symmetrical': 'False', 'through': "orm['team.Member']", 'to': "orm['auth.User']"}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['competition']
