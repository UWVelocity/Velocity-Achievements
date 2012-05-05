# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Term'
        db.create_table('achievements_term', (
            ('term', self.gf('django.db.models.fields.CharField')(max_length=5, primary_key=True)),
        ))
        db.send_create_signal('achievements', ['Term'])

        # Adding field 'Nomination.term'
        db.add_column('achievements_nomination', 'term',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievements.Term'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Grant.term'
        db.add_column('achievements_grant', 'term',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievements.Term'], null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting model 'Term'
        db.delete_table('achievements_term')

        # Deleting field 'Nomination.term'
        db.delete_column('achievements_nomination', 'term_id')

        # Deleting field 'Grant.term'
        db.delete_column('achievements_grant', 'term_id')

    models = {
        'achievements.achievement': {
            'Meta': {'object_name': 'Achievement'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'svg_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'achievements.grant': {
            'Meta': {'unique_together': "(('achievement', 'participant'),)", 'object_name': 'Grant'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Achievement']"}),
            'granted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Participant']"}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Term']", 'null': 'True', 'blank': 'True'})
        },
        'achievements.nomination': {
            'Meta': {'unique_together': "(('achievement', 'participant', 'nominator'),)", 'object_name': 'Nomination'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Achievement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nominator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['achievements.Participant']"}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Participant']"}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Term']", 'null': 'True', 'blank': 'True'})
        },
        'achievements.participant': {
            'Meta': {'object_name': 'Participant', '_ormbases': ['emailauth.UserWithEmail']},
            'userwithemail_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['emailauth.UserWithEmail']", 'unique': 'True', 'primary_key': 'True'})
        },
        'achievements.render': {
            'Meta': {'unique_together': "(('achievement', 'width', 'height'),)", 'object_name': 'Render'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Achievement']"}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'achievements.term': {
            'Meta': {'object_name': 'Term'},
            'term': ('django.db.models.fields.CharField', [], {'max_length': '5', 'primary_key': 'True'})
        },
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'emailauth.userwithemail': {
            'Meta': {'object_name': 'UserWithEmail', '_ormbases': ['auth.User']},
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['achievements']