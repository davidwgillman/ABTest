from django.db import models
from django import forms
from datetime import datetime

from django.core import urlresolvers
from django.core.exceptions import ValidationError
from django.forms.formsets import BaseFormSet

class Step(models.Model) :
	name = models.CharField(max_length=50)
	number = models.IntegerField(default=1)

	def __unicode__(self) :
		return self.name

	class Meta:
		ordering = ['number']


BOOLEAN_LABEL = 'True/False'
FLOAT_LABEL = 'Number'

class StepOutcome(models.Model) :
        VALUE_TYPES = (
        (BOOLEAN_LABEL, BOOLEAN_LABEL),
        (FLOAT_LABEL, FLOAT_LABEL)
)
        
	step = models.ForeignKey(Step)
	name = models.CharField(max_length=50)
	valueType = models.CharField(max_length=50, blank=False, null=False,
                                     choices=VALUE_TYPES)

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
	step = models.ForeignKey(Step, related_name='nextstepcondition_set')

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

        def clean(self, *args, **kwargs):
                if self.comparator1 and self.comparator1 != TRUE and self.comparator1 != FALSE and self.valueToCompare1 == '':
                        raise ValidationError(
                                ("Fill in Value1."))
                elif self.comparator2 and not self.comparator1:
                        raise ValidationError(
                                ("Fill in the first comparator before the second."))
                elif self.comparator2 and self.comparator2 != TRUE and self.comparator2 != FALSE and self.valueToCompare2 == '':
                        raise ValidationError(
                                ("Fill in Value2."))
                elif self.dependsOnStepNotDone and self.dependsOnOutcome:
                        raise ValidationError(
                                ("A next step condition may depend on either a step not being done, or an outcome value. Not both."))
                elif self.dependsOnStepNotDone:
                        if not self.stepNotDone:
                                raise ValidationError(
                                ("Enter the step not done."))
                elif self.dependsOnOutcome:
                        if not self.conditionalOutcome:
                                raise ValidationError(
                                ("Enter the outcome to be tested."))

                        
                super(NextStepCondition, self).clean(*args, **kwargs)
                
        def __init__(self, *args, **kwargs):
                super(NextStepCondition, self).__init__(*args, **kwargs)
                #self.priority = NextStepCondition.objects.filter(step=self.step).count()+1 #Not working yet..
                
	def __unicode__(self) :
		return unicode(self.step) 
	

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

        def clean(self, *args, **kwargs):
                '''
                This can check if both Last and Current boolean fields have been checked.
                If that happens, that's definitely an error. But at the time of this
                cleaning, not all the other model changes are inputted yet. Thus, if
                a nurse changes a patient's double-last setup so that the second
                Patient Step down the list is changed to current; that's a perfectly
                valid change logically, but if we tried to check the "last" boolean
                status of other patient steps for this patient, the first Patient
                Step would get called here and would return a ValidationError,
                because the change in the boolean field for the second step hasn't
                been saved yet. All of that to say -- any validating to ensure
                that no patient has more than one patient step with a last or
                current boolean field check-marked, must take place at the
                formset level. But for the Admin page, that's within the Admin's
                automatic formset, which I don't have access to unless I make a
                custom Admin. Which I'd rather not. So what I've done, is overriden
                the save method to set all other boolean fields of the same type
                being checked, to False, which hopefully the nurse was doing anyway.
                It might confuse a nurse if they don't realize why their change
                made a previous Last button become unchecked, as this doesn't show
                any error messages, which is less than ideal, but it works for now.
                -NJ
                '''
                if self.last and self.current:
                        raise ValidationError(("Only one of these can be true!"))
                super(PatientStep, self).clean(*args, **kwargs)
                
	def save(self, *args, **kwargs):            
                if self.last:
                        PatientStep.objects.filter(last=True, patient=self.patient).update(last=False)
                        
                elif self.current:
                        PatientStep.objects.filter(current=True,
                                                   patient=self.patient).update(current=False)
                        
                
                super(PatientStep, self).save(*args, **kwargs)

        def __unicode__(self) :
                return unicode(self.step)

        class Meta:
                ordering = ['step__name']



class PatientOutcome(models.Model):
	patient = models.ForeignKey(Patient)
	stepOutcome = models.ForeignKey(StepOutcome)
	
	value = models.CharField(max_length=50)


	def __unicode__(self) :
		return unicode(self.stepOutcome)

BOOLEAN_CHOICES = (
        (TRUE, 'True'),
        (FALSE, 'False'),
        )
class PatientOutcomeForm(forms.Form) :
        stepOutcome = forms.ModelChoiceField(queryset=StepOutcome.objects.all(),
                                        widget=forms.HiddenInput())
        value = forms.CharField(label='Value', max_length=50)
        

        def clean(self): #Validate that the value inputted matches up with the ValueType.
                cleaned_data = super(PatientOutcomeForm, self).clean()
                value = cleaned_data.get('value')
                value_type = cleaned_data.get('stepOutcome').valueType
                if value_type == BOOLEAN_LABEL:
                        if value != TRUE and value != FALSE:
                                raise forms.ValidationError(
                                        ('Data for this outcome must be %(v_t)s'),
                                                code="Wrong data type",
                                                params={'v_t': BOOLEAN_LABEL},
                                                )
                elif value_type == FLOAT_LABEL:
                        try:
                                float(value)
                        except (ValueError, TypeError):
                                raise forms.ValidationError(
                                        ('Data for this outcome must be a %(v_t)s'),
                                                code="Wrong data type",
                                                params={'v_t': FLOAT_LABEL},
                                                )
                return cleaned_data
    
        def __init__(self, *args, **kwargs):
                super(PatientOutcomeForm, self).__init__(*args, **kwargs)
                
                s_o = self.initial.get('stepOutcome')
                if s_o:
                        if s_o.valueType == BOOLEAN_LABEL:
                                self.fields['value'] = forms.ChoiceField(choices=BOOLEAN_CHOICES)

                        self.fields['value'].label = unicode(s_o)
                        
                

'''
class BasePatientOutcomeFormSet(BaseFormSet):
        def add_fields(self, form, index):
                super(BasePatientOutcomeFormSet, self).add_fields(form, index)
                form.fields['patient'] = forms.ModelChoiceField(queryset=Patient.objects.all(),
                                         widget=forms.HiddenInput())
'''

class PatientFlag (models.Model):
        stepOutcome = models.ForeignKey(StepOutcome)
        comparator1 = models.CharField(max_length=2, choices=COMPARATOR_CHOICES)
	valueToCompare1 = models.CharField(max_length=50, blank=True)
	comparator2 = models.CharField(max_length=2, blank=True, choices=COMPARATOR_CHOICES)
	valueToCompare2 = models.CharField(max_length=50, blank=True)
        level = models.CharField('Warning Level', max_length=50, blank=True, choices=FLAG_LEVEL_CHOICES)
	name = models.CharField('Outcome Name', max_length=50)

        def __unicode__(self) :
                return unicode(self.name)

class PatientForm(forms.ModelForm):

        
        class Meta:
                model = Patient
                fields = ['name', 'dob', 'timeIn']
                error_messages = {
                        'dob': {
                                'invalid': "Invalid date. Use format M/D/Y."
                                }
                        }

        def clean(self):
                cleaned_data = super(PatientForm, self).clean()
                name = cleaned_data.get('name')
                dob = cleaned_data.get('dob')

                patients = Patient.objects.all()
                for patient in patients:
                        if patient.name == name and patient.dob == dob:
                                raise forms.ValidationError(
                                        ('A patient with this name and D.O.B. already exists.')
                                        )
                return cleaned_data
                        
'''                
class DeletePatientForm(forms.ModelForm):
        class Meta:
                model = Patient
                fields = []

'''    
