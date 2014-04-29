from django.shortcuts import render
from django.http import HttpResponse

from tracker.models import Step, StepOutcome, NextStepCondition, FlagCondition
from tracker.models import Patient, PatientStep, PatientOutcome

def index(request):
	patientList = Patient.objects.order_by('name')
	output = ', '.join([unicode((p.name, p.dob)) for p in patientList])
    	return HttpResponse(output)

def detail(request, patient_id):
    return HttpResponse("You're looking at patient %s." % patient_id)


