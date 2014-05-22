# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'PatientFlag.valueToCompare1'
        db.delete_column(u'tracker_patientflag', 'valueToCompare1')

        # Deleting field 'PatientFlag.valueToCompare2'
        db.delete_column(u'tracker_patientflag', 'valueToCompare2')

        # Deleting field 'PatientFlag.stepOutcome'
        db.delete_column(u'tracker_patientflag', 'stepOutcome_id')

        # Deleting field 'PatientFlag.comparator2'
        db.delete_column(u'tracker_patientflag', 'comparator2')

        # Deleting field 'PatientFlag.comparator1'
        db.delete_column(u'tracker_patientflag', 'comparator1')

        # Adding field 'PatientFlag.patient'
        db.add_column(u'tracker_patientflag', 'patient',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Patient'], null=True),
                      keep_default=False)


        # Changing field 'PatientFlag.name'
        db.alter_column(u'tracker_patientflag', 'name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    def backwards(self, orm):
        # Adding field 'PatientFlag.valueToCompare1'
        db.add_column(u'tracker_patientflag', 'valueToCompare1',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'PatientFlag.valueToCompare2'
        db.add_column(u'tracker_patientflag', 'valueToCompare2',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'PatientFlag.stepOutcome'
        db.add_column(u'tracker_patientflag', 'stepOutcome',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.StepOutcome'], null=True),
                      keep_default=False)

        # Adding field 'PatientFlag.comparator2'
        db.add_column(u'tracker_patientflag', 'comparator2',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PatientFlag.comparator1'
        db.add_column(u'tracker_patientflag', 'comparator1',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True),
                      keep_default=False)

        # Deleting field 'PatientFlag.patient'
        db.delete_column(u'tracker_patientflag', 'patient_id')


        # Changing field 'PatientFlag.name'
        db.alter_column(u'tracker_patientflag', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=50))

    models = {
        u'tracker.flagcondition': {
            'Meta': {'object_name': 'FlagCondition'},
            'comparator1': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'comparator2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Step']"}),
            'stepOutcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.StepOutcome']"}),
            'valueToCompare1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
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
            'step': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nextstepcondition_set'", 'to': u"orm['tracker.Step']"}),
            'stepNotDone': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'stepNotDone'", 'null': 'True', 'to': u"orm['tracker.Step']"}),
            'valueToCompare1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'valueToCompare2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'tracker.patient': {
            'Meta': {'object_name': 'Patient'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'timeIn': ('django.db.models.fields.DateTimeField', [], {}),
            'timeOut': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'tracker.patientflag': {
            'Meta': {'object_name': 'PatientFlag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Patient']", 'null': 'True'})
        },
        u'tracker.patientoutcome': {
            'Meta': {'object_name': 'PatientOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Patient']"}),
            'stepOutcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.StepOutcome']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'tracker.patientstep': {
            'Meta': {'ordering': "['step__name']", 'object_name': 'PatientStep'},
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'valueType': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['tracker']