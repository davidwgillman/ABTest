# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PatientStep'
        db.create_table(u'tracker_patientstep', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('step', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Step'])),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Patient'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'tracker', ['PatientStep'])

        # Adding model 'PatientOutcome'
        db.create_table(u'tracker_patientoutcome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patientStep', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.PatientStep'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'tracker', ['PatientOutcome'])

        # Adding model 'Patient'
        db.create_table(u'tracker_patient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('timeIn', self.gf('django.db.models.fields.DateTimeField')()),
            ('timeOut', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'tracker', ['Patient'])

        # Adding field 'FlagCondition.level'
        db.add_column(u'tracker_flagcondition', 'level',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'PatientStep'
        db.delete_table(u'tracker_patientstep')

        # Deleting model 'PatientOutcome'
        db.delete_table(u'tracker_patientoutcome')

        # Deleting model 'Patient'
        db.delete_table(u'tracker_patient')

        # Deleting field 'FlagCondition.level'
        db.delete_column(u'tracker_flagcondition', 'level')


    models = {
        u'tracker.flagcondition': {
            'Meta': {'object_name': 'FlagCondition'},
            'comparator1': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'comparator2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'stepOutcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.StepOutcome']"}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'valueToCompare1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'valueToCompare2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'tracker.nextstepcondition': {
            'Meta': {'object_name': 'NextStepCondition'},
            'comparator1': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'comparator2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'conditionalOutcome': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conditionalOutcome'", 'null': 'True', 'to': u"orm['tracker.StepOutcome']"}),
            'dependsOnOutcome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dependsOnStepNotDone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nextStep': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nextStep'", 'to': u"orm['tracker.Step']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Step']"}),
            'stepNotDone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stepNotDone'", 'null': 'True', 'to': u"orm['tracker.Step']"}),
            'valueToCompare1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'valueToCompare2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'tracker.patient': {
            'Meta': {'object_name': 'Patient'},
            'dob': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'timeIn': ('django.db.models.fields.DateTimeField', [], {}),
            'timeOut': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'tracker.patientoutcome': {
            'Meta': {'object_name': 'PatientOutcome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'patientStep': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.PatientStep']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '25'})
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
            'Meta': {'object_name': 'Step'},
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