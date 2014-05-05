from django.db import models

class Step(models.Model) :
	name = models.CharField(max_length=50)
	number = models.IntegerField(default=1)

	def __unicode__(self) :
		return self.name

	class Meta:
		ordering = ['number']

class StepOutcome(models.Model) :
	step = models.ForeignKey(Step)
	name = models.CharField(max_length=50)
	valueType = models.CharField(max_length=50, blank=True)

	def __unicode__(self) :
		return unicode(self.step) + " Outcomes"

COMPARATOR_CHOICES = (
	('<', 'less than'),
	('<=', 'less than or equal to'),
	('==', 'equal to'),
	('>', 'greater than'),
	('>=', 'greater than or equal to')
)

class NextStepCondition(models.Model) :
	step = models.ForeignKey(Step, related_name='step') 
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
		return unicode(self.step) + " Next-step Conditions"

class FlagCondition(models.Model) :
	name = models.CharField(max_length=50)
	stepOutcome = models.ForeignKey(StepOutcome)
	comparator1 = models.CharField(max_length=2)
	valueToCompare1 = models.CharField(max_length=50)
	comparator2 = models.CharField(max_length=2, blank=True)
	valueToCompare2 = models.CharField(max_length=50, blank=True)
	value = models.BooleanField(default=False)
	level = models.CharField('Warning Level', max_length=50, blank=True)

	def __unicode__(self) :
		return self.name

class Patient(models.Model):
	name = models.CharField('Last, First', max_length=200)
	dob = models.DateField('Date of Birth')
	timeIn = models.DateTimeField('Time In')
	timeOut = models.DateTimeField('Time Out', null=True, blank=True)

	def __unicode__(self) :
		return self.name + ' -- DOB ' + self.dob.strftime('%Y-%m-%d')

class PatientStep(models.Model):
	step = models.ForeignKey(Step)
	patient = models.ForeignKey(Patient)
	start = models.DateTimeField('Start Time', null=True, blank=True)
	end = models.DateTimeField('End Time', null=True, blank=True)

	def __unicode__(self) :
		return unicode(self.patient) + ' -- ' +  unicode(self.step)

class PatientOutcome(models.Model):
	patientStep = models.ForeignKey(PatientStep)
	name = models.CharField('Outcome Name', max_length=50)
	value = models.CharField('Outcome Value', max_length=50)

	def __unicode__(self) :
		return unicode(self.patientStep) + ' -- ' + self.name


