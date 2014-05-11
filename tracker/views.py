from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from tracker.models import Step, StepOutcome, NextStepCondition, FlagCondition
from tracker.models import Patient, PatientStep, PatientOutcome, PatientForm

from datetime import datetime

def everything_tracker(request):
    if request.method == 'POST': # If the form has been submitted...
        input_form = PatientForm(request.POST) # A form bound to the POST data
        if input_form.is_valid(): # All validation rules pass
            new_p = Patient.objects.create(name=input_form.cleaned_data['name'],
                                   dob=input_form.cleaned_data['dob'],
                                   timeIn=input_form.cleaned_data['timeIn'],
                                           current_step=Step.objects.get(number=1)
                                           )
            #input_form.save() #This line was making a duplicate patient object.
                                # I don't know why?? Anyway, do we need this line?
            #return HttpResponseRedirect('thanks/') # Redirect after POST
            
    form = PatientForm(initial={'timeIn': datetime.now()}) # Blank form to add a new patient
    patient_list = Patient.objects.all()
    return render(request, 'tracker/tracker_template.html', {'form': form, 'PatientList': patient_list})

# def bootstrap(request):

def detail(request, patient_id):
    return HttpResponse("You're looking at patient %s." % patient_id)

def thanks(request):
    return HttpResponse("Thanks for adding a patient.")



