# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Step'
        db.create_table(u'tracker_step', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'tracker', ['Step'])

        # Adding model 'StepOutcome'
        db.create_table(u'tracker_stepoutcome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('step', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Step'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('valueType', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'tracker', ['StepOutcome'])

        # Adding model 'NextStepCondition'
        db.create_table(u'tracker_nextstepcondition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('step', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Step'])),
            ('priority', self.gf('django.db.models.fields.IntegerField')()),
            ('dependsOnStepNotDone', self.gf('django.db.models.fields.BooleanField')()),
            ('stepNotDone', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stepNotDone', null=True, to=orm['tracker.Step'])),
            ('dependsOnOutcome', self.gf('django.db.models.fields.BooleanField')()),
            ('conditionalOutcome', self.gf('django.db.models.fields.related.ForeignKey')(related_name='conditionalOutcome', null=True, to=orm['tracker.StepOutcome'])),
            ('comparator1', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('valueToCompare1', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('comparator2', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('valueToCompare2', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('nextStep', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nextStep', to=orm['tracker.Step'])),
        ))
        db.send_create_signal(u'tracker', ['NextStepCondition'])

        # Adding model 'FlagCondition'
        db.create_table(u'tracker_flagcondition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('stepOutcome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.StepOutcome'])),
            ('comparator1', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('valueToCompare1', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('comparator2', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('valueToCompare2', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('value', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'tracker', ['FlagCondition'])


    def backwards(self, orm):
        # Deleting model 'Step'
        db.delete_table(u'tracker_step')

        # Deleting model 'StepOutcome'
        db.delete_table(u'tracker_stepoutcome')

        # Deleting model 'NextStepCondition'
        db.delete_table(u'tracker_nextstepcondition')

        # Deleting model 'FlagCondition'
        db.delete_table(u'tracker_flagcondition')


    models = {
        u'tracker.flagcondition': {
            'Meta': {'object_name': 'FlagCondition'},
            'comparator1': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'comparator2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'stepOutcome': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.StepOutcome']"}),
            'value': ('django.db.models.fields.BooleanField', [], {}),
            'valueToCompare1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'valueToCompare2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'tracker.nextstepcondition': {
            'Meta': {'object_name': 'NextStepCondition'},
            'comparator1': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'comparator2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'conditionalOutcome': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conditionalOutcome'", 'null': 'True', 'to': u"orm['tracker.StepOutcome']"}),
            'dependsOnOutcome': ('django.db.models.fields.BooleanField', [], {}),
            'dependsOnStepNotDone': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nextStep': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nextStep'", 'to': u"orm['tracker.Step']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Step']"}),
            'stepNotDone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stepNotDone'", 'null': 'True', 'to': u"orm['tracker.Step']"}),
            'valueToCompare1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'valueToCompare2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'tracker.step': {
            'Meta': {'object_name': 'Step'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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