from django.contrib import admin

from tracker.models import Step, StepOutcome, NextStepCondition, FlagCondition
from tracker.models import Patient, PatientStep, PatientOutcome, PatientFlag

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
	fields = ('step', 'priority',
                  ('dependsOnStepNotDone', 'stepNotDone'),
                  ('dependsOnOutcome', 'conditionalOutcome'),
                  ('comparator1', 'valueToCompare1'),
                  ('comparator2', 'valueToCompare2'),
                  'nextStep')

class FlagConditionInline(admin.StackedInline) :
        model = FlagCondition
        extra = 0
        #fk_name = 'step'
        fields = ('step', 'name', 'stepOutcome',
                  ('comparator1', 'valueToCompare1'),
                  ('comparator2', 'valueToCompare2'), 'level')
                  
        

class StepAdmin(admin.ModelAdmin) :
	list_display = ('name',)
	inlines = [StepOutcomeInline, NextStepConditionInline,
                   FlagConditionInline]

admin.site.register(Step, StepAdmin)

'''
class PatientOutcomeInline(admin.StackedInline):
        model = PatientOutcome
        max_num = 1

class PatientStepAdmin(admin.ModelAdmin):
        inlines = [PatientOutcomeInline,]
        #list_display = ('patient', 'step')
        
admin.site.register(PatientStep, PatientStepAdmin)

class PatientStepLinkInline(admin.StackedInline):
        model = PatientStep
        fields = (('last', 'current'), 'step', 'changeform_link', 'start', 'end')
        readonly_fields = ('changeform_link',)

class PatientAdmin(admin.ModelAdmin):
        #date_hierarchy = 'timeIn'
        inlines = [PatientStepLinkInline,]
        fields = (('name', 'dob'),('timeIn', 'timeOut'))

admin.site.register(Patient, PatientAdmin)


'''
class PatientStepInline(admin.StackedInline) :
	model = PatientStep
	extra = 0

class PatientOutcomeInline(admin.StackedInline) :
        model = PatientOutcome
        fk_name = 'patient'
        extra = 0

class PatientFlagInline(admin.StackedInline) :
        model = PatientFlag
        fk_name = 'patient'
        extra = 0


class PatientAdmin(admin.ModelAdmin) :
        #date_hierarchy = 'timeIn'
	inlines = [PatientStepInline, PatientOutcomeInline]
	fields = (('name', 'dob'),('timeIn', 'timeOut')) 

admin.site.register(Patient, PatientAdmin)

