from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from tracker.models import Step, StepOutcome, NextStepCondition, FlagCondition
from tracker.models import Patient, PatientStep, PatientOutcome, PatientForm

from datetime import datetime

def everything_tracker(request):
    
    if request.method == 'POST': # If a form has been submitted.
        if 'Add Patient' in request.POST:
            form = PatientForm(request.POST) # A PatientForm bound to the POST data.
            if form.is_valid(): # If validation rules pass
                new_p = Patient.objects.create(name=form.cleaned_data['name'],
                                       dob=form.cleaned_data['dob'],
                                       timeIn=form.cleaned_data['timeIn'],
                                       current_step=Step.objects.get(number=1) )
                #form.save() #This line was making a duplicate patient object. Do we need this line?
                return HttpResponseRedirect(reverse('everything_tracker')) # Redirect to the same view
            else:
                print form.errors
            
        elif 'SUBMIT_FORM_DATA_DUMMY_VAR' in request.POST:
            pass #This is where we can handle other buttons being pressed.
        
    else:
        form = PatientForm(initial={'timeIn': datetime.now()}) # Blank form to add a new patient
            
    patient_list = Patient.objects.all()
    return render(request, 'tracker/CSSTracker.html', {'form': form, 'patient_list': patient_list})

def detail(request, patient_id):
    return HttpResponse("You're looking at patient %s." % patient_id)

def thanks(request):
    return HttpResponse("Thanks for adding a patient.")



