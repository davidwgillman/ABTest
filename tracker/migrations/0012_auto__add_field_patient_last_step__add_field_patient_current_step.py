# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Patient.last_step'
        db.add_column(u'tracker_patient', 'last_step',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='last_step', null=True, to=orm['tracker.Step']),
                      keep_default=False)

        # Adding field 'Patient.current_step'
        db.add_column(u'tracker_patient', 'current_step',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='current_step', null=True, to=orm['tracker.Step']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Patient.last_step'
        db.delete_column(u'tracker_patient', 'last_step_id')

        # Deleting field 'Patient.current_step'
        db.delete_column(u'tracker_patient', 'current_step_id')


    models = {
        u'tracker.flagcondition': {
            'Meta': {'object_name': 'FlagCondition'},
            'comparator1': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'comparator2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'stepOutcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.StepOutcome']"}),
            'valueToCompare1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'valueToCompare2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'tracker.nextstepcondition': {
            'Meta': {'object_name': 'NextStepCondition'},
            'comparator1': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'comparator2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'conditionalOutcome': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conditionalOutcome'", 'null': 'True', 'to': u"orm['tracker.StepOutcome']"}),
            'dependsOnOutcome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dependsOnStepNotDone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nextStep': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nextStep'", 'to': u"orm['tracker.Step']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'step'", 'to': u"orm['tracker.Step']"}),
            'stepNotDone': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'stepNotDone'", 'null': 'True', 'to': u"orm['tracker.Step']"}),
            'valueToCompare1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'valueToCompare2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'tracker.patient': {
            'Meta': {'object_name': 'Patient'},
            'current_step': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'current_step'", 'null': 'True', 'to': u"orm['tracker.Step']"}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_step': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'last_step'", 'null': 'True', 'to': u"orm['tracker.Step']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'timeIn': ('django.db.models.fields.DateTimeField', [], {}),
            'timeOut': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'tracker.patientoutcome': {
            'Meta': {'object_name': 'PatientOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'patientStep': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.PatientStep']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'tracker.patientstep': {
            'Meta': {'object_name': 'PatientStep'},
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Patient']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Step']"})
        },
        u'tracker.step': {
            'Meta': {'ordering': "['number']", 'object_name': 'Step'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'tracker.stepoutcome': {
            'Meta': {'object_name': 'StepOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Step']"}),
            'valueType': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['tracker']