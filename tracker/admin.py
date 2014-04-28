from django.contrib import admin

from tracker.models import Step, StepOutcome, NextStepCondition, FlagCondition

admin.site.register(Step)
admin.site.register(StepOutcome)
admin.site.register(NextStepCondition)
admin.site.register(FlagCondition)


