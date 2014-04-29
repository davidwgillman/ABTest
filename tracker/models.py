from django.db import models

class Step(models.Model) :
	name = models.CharField(max_length=50)
	number = models.IntegerField(default=1)

	def __unicode__(self) :
		return self.name

class StepOutcome(models.Model) :
	step = models.ForeignKey(Step)
	name = models.CharField(max_length=50)
	valueType = models.CharField(max_length=50, blank=True)

	def __unicode__(self) :
		return unicode(self.step) + " Outcomes"

class NextStepCondition(models.Model) :
	step = models.ForeignKey(Step, related_name='step') 
	priority = models.IntegerField(default=1) # conditions are evaluated in order
	dependsOnStepNotDone = models.BooleanField(default=False)
	stepNotDone = models.ForeignKey(Step, null=True, related_name='stepNotDone')
	dependsOnOutcome = models.BooleanField(default=False)
	conditionalOutcome = models.ForeignKey(StepOutcome, null=True, related_name='conditionalOutcome')
	comparator1 = models.CharField(max_length=2, blank=True)
	valueToCompare1 = models.CharField(max_length=50, blank=True)
	comparator2 = models.CharField(max_length=2, blank=True)
	valueToCompare2 = models.CharField(max_length=50, blank=True)
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
		return self.name

class PatientStep(models.Model):
	step = models.ForeignKey(Step)
	patient = models.ForeignKey(Patient)
	start = models.DateTimeField('Start Time', null=True, blank=True)
	end = models.DateTimeField('End Time', null=True, blank=True)

	def __unicode__(self) :
		return unicode(self.step)

class PatientOutcome(models.Model):
	patientStep = models.ForeignKey(PatientStep)
	stepOutcome = models.ForeignKey(StepOutcome)
	value = models.CharField('Outcome Value', max_length=25)

	def __unicode__(self) :
		return unicode(self.stepOutcome)


