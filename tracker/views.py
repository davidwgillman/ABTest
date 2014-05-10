from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from tracker.models import Step, StepOutcome, NextStepCondition, FlagCondition
from tracker.models import Patient, PatientStep, PatientOutcome, PatientForm

def index(request):
    if request.method == 'POST': # If the form has been submitted...
        form = PatientForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect('thanks/') # Redirect after POST
    else:
        form = PatientForm() # An unbound form

    return render(request, 'tracker/index.html', {'form': form})

# def bootstrap(request):

def detail(request, patient_id):
    return HttpResponse("You're looking at patient %s." % patient_id)

def thanks(request):
    return HttpResponse("Thanks for adding a patient.")



