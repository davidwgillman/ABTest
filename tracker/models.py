from django.db import models
from django import forms
from datetime import datetime

from django.core import urlresolvers

class Step(models.Model) :
	name = models.CharField(max_length=50)
	number = models.IntegerField(default=1)

	def __unicode__(self) :
		return self.name

	class Meta:
		ordering = ['number']



class StepOutcome(models.Model) :
        BOOLEAN = 'boolean'
        FLOAT = 'float'
        VALUE_TYPES = (
        (BOOLEAN, 'True/False'),
        (FLOAT, 'Number')
)
        
	step = models.ForeignKey(Step)
	name = models.CharField(max_length=50)
	valueType = models.CharField(max_length=50, blank=True, choices=VALUE_TYPES)

	def __unicode__(self) :
		return unicode(self.name) #+ " Outcome"



# NJ: Why do these have to be strings of length 2 or less?
# DG: This is used by more than one class, and each attribute is declared with max_length=2
# True and False are built-in Python boolean values.
TRUE = 'TR'
FALSE = 'FA'
COMPARATOR_CHOICES = (
	('<', 'less than'),
	('<=', 'less than or equal to'),
	('==', 'equal to'),
	('>', 'greater than'),
	('>=', 'greater than or equal to'),
        (TRUE, 'True'),
        (FALSE, 'False')
)


	
class NextStepCondition(models.Model) :
	step = models.ForeignKey(Step, related_name='step')

	# Use that number plus one, for the default priority when a new condition is made in the admin page.
	priority = models.IntegerField(default=1) # conditions are evaluated in order
	dependsOnStepNotDone = models.BooleanField(default=False)
	stepNotDone = models.ForeignKey(Step, null=True, blank=True, related_name='stepNotDone')
	dependsOnOutcome = models.BooleanField(default=False)
	conditionalOutcome = models.ForeignKey(StepOutcome, null=True, blank=True, related_name='conditionalOutcome')
	comparator1 = models.CharField('Cmp1', max_length=2, blank=True, choices=COMPARATOR_CHOICES)
	valueToCompare1 = models.CharField('Value1', max_length=50, blank=True)
	comparator2 = models.CharField('Cmp2', max_length=2, blank=True, choices=COMPARATOR_CHOICES)
	valueToCompare2 = models.CharField('Value2', max_length=50, blank=True)
	nextStep = models.ForeignKey(Step, related_name='nextStep')

	def __unicode__(self) :
		return unicode(self.step) 

	# Need to figure out how to use this. Having trouble here. I want this called each time a
	# NextStepCondition object is made.
	def get_default_priority(st):
                List_of_previous_objects = NextStepCondition.objects.filter(step__name=st)
                default_priority = List_of_previous_objects.count() + 1
                return default_priority
	

FLAG_LEVEL_CHOICES = (
	('1', 'Warning'),
	('2', 'Emergency')
)
        
class FlagCondition(models.Model) :
	name = models.CharField(max_length=50)
	stepOutcome = models.ForeignKey(StepOutcome)
	comparator1 = models.CharField(max_length=2, choices=COMPARATOR_CHOICES)
	valueToCompare1 = models.CharField(max_length=50, blank=True)
	comparator2 = models.CharField(max_length=2, blank=True, choices=COMPARATOR_CHOICES)
	valueToCompare2 = models.CharField(max_length=50, blank=True)
	level = models.CharField('Warning Level', max_length=50, blank=True, choices=FLAG_LEVEL_CHOICES)

	def __unicode__(self) :
		return self.name


class Patient(models.Model):
	name = models.CharField('Last, First', max_length=200)
	dob = models.DateField(verbose_name='Date of Birth')
	timeIn = models.DateTimeField('Time In')
	timeOut = models.DateTimeField('Time Out', null=True, blank=True)

	def __unicode__(self) :
		return self.name + ' -- DOB ' + self.dob.strftime('%Y-%m-%d')

	
class PatientStep(models.Model):
        last = models.BooleanField(default=False)
        current = models.BooleanField(default=False)
        patient = models.ForeignKey(Patient)
	step = models.ForeignKey(Step)
	start = models.DateTimeField('Start Time', null=True, blank=True)
	end = models.DateTimeField('End Time', null=True, blank=True)

        def __unicode__(self) :
                return unicode(self.patient) + ' -- ' + unicode(self.step)
        
	def changeform_link(self):
                if self.id:
                        changeform_url = urlresolvers.reverse(
                                'admin:tracker_patientstep_change',
                                args=(self.id,) )
                        return u'<a href="%s" target="_blank">Outcome</a>' % changeform_url
                else:
                        return u''

        changeform_link.allow_tags = True
        changeform_link.short_description = '' #omits column header

        class Meta:
                ordering = ['patient__name']



class PatientOutcome(models.Model):
	patientStep = models.ForeignKey(PatientStep)
	
	#name = models.CharField('Outcome Name', max_length=50)
	value = models.CharField('Outcome Value', max_length=50)


	def __unicode__(self) :
		return unicode(self.patientStep)

# Add PatientFlag class

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'dob', 'timeIn']
        error_messages = {
                'dob': {
                        'invalid': "Invalid date. Use format M/D/Y."
                        }
                }


