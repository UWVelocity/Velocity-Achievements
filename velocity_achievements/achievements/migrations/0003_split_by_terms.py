# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

def past_term_key_for_date(date):
    year = date.year
    month = date.month - 1
    month = (month - 4)
    if month < 0:
        year -= 1
        month %= 12
    t="WSF"[month/4] # Math is magic
    return t + str(date.year)

def current_term_key_for_date(date):
    t="WSF"[(date.month - 1)/4] # Math is magic
    return t + str(date.year)

class Migration(DataMigration):

    def forwards(self, orm):
        today = datetime.date.today()
        past_term = past_term_key_for_date(today)
        orm.Term.objects.get_or_create(term=past_term)
        orm.Term.objects.get_or_create(term=current_term_key_for_date(today))
        orm.Nomination.objects.all().update(term=past_term)
        orm.Grant.objects.all().update(term=past_term)

    def backwards(self, orm):
        "Nothing to do!"
        pass

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
    symmetrical = True
