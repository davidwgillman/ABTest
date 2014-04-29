from django.contrib import admin

from tracker.models import Step, StepOutcome, NextStepCondition, FlagCondition
from tracker.models import Patient, PatientStep, PatientOutcome

# django.contrib.admin doesn't have nested inlines like
#
# Step
#  \-> StepOutcome
#       \-> FlagCondition
#
# or
#
# Patient
#  \-> PatientStep
#       \-> PatientOutcome
#
# To implement this, we would need to make a StackedInline class that can be registered.
#

class StepOutcomeInline(admin.StackedInline) :
	model = StepOutcome
	extra = 0
	fields = (('name', 'valueType'),) 

class NextStepConditionInline(admin.StackedInline) :
	model = NextStepCondition
	extra = 0
	fk_name = 'step'
	fields = 	('step', ('priority', 'nextStep'), ('dependsOnStepNotDone', 'stepNotDone'),
				('dependsOnOutcome', 'conditionalOutcome'), 
				('comparator1', 'valueToCompare1'), 
				('comparator2', 'valueToCompare2')
			)

class StepAdmin(admin.ModelAdmin) :
	list_display = ('name',)
	inlines = [StepOutcomeInline, NextStepConditionInline]

admin.site.register(Step, StepAdmin)
#admin.site.register(StepOutcome)
#admin.site.register(NextStepCondition)
admin.site.register(FlagCondition)

class PatientStepInline(admin.StackedInline) :
	model = PatientStep
	extra = 0

class PatientAdmin(admin.ModelAdmin) :
	inlines = [PatientStepInline]

admin.site.register(Patient, PatientAdmin)
#admin.site.register(PatientStep)
admin.site.register(PatientOutcome)

