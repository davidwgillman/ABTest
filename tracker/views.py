from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect

from tracker.models import Step, StepOutcome, NextStepCondition, FlagCondition
from tracker.models import Patient, PatientStep, PatientOutcome, PatientForm

from django.utils import timezone

def everything_tracker(request):
    context_dict = {}
    #context_dict.update(csrf(request)) #Actually it seems that this is handled by the render function.
    if request.method == 'POST': # If a form has been submitted.
        
        if 'Add Patient' in request.POST:
            form = PatientForm(request.POST) # A PatientForm bound to the POST data.
            if form.is_valid(): # If validation rules pass
                new_p = Patient.objects.create(name=form.cleaned_data['name'],
                                       dob=form.cleaned_data['dob'],
                                       timeIn=form.cleaned_data['timeIn'] )

                #Associate a new PatientStep with the newly created patient, and start it on the
                # first step as defined in the Admin page.
                first_step = Step.objects.get(number=1)
                p_step = PatientStep(step=first_step, patient=new_p,
                                       current=True, start=timezone.now())
                p_step.save()
        
                return HttpResponseRedirect(reverse('everything_tracker')) # Redirect to the same view
            else:
                pass #Just let the bound form with invalid data go to the very end, to display errors.
            
        elif 'SUBMIT_FORM_DATA_DUMMY_VAR' in request.POST:
            pass #This is where we can handle other buttons being pressed.
        
    else:
        form = PatientForm(initial={'timeIn': timezone.now()}) # Blank form to add a new patient
            
    # Can order these patients in ascending or descending order of arrival    
    patient_objects = Patient.objects.all().order_by('-timeIn')
    patient_list = []
    for p in patient_objects:
        try:
            last_step = p.patientstep_set.get(last=True)
        except PatientStep.DoesNotExist:
            last_step = "None"
        except PatientStep.MultipleObjectsReturned:
            last_step = "None"
            #Raise some error that doesn't crash everything?
            
        try:
            current_step = p.patientstep_set.get(current=True)
        except PatientStep.DoesNotExist:
            #Could raise an error here, or just display None as well.
            #Either way this shouldn't happen.
            current_step = 'None'
        except PatientStep.MultipleObjectsReturned:
            current_step = 'None'
            # What do we want to do here?
            
        t = (p, last_step, current_step)
        patient_list.append(t)
    
        
    context_dict['form'] = form
    context_dict['patient_list'] = patient_list
    return render(request, 'tracker/CSSTracker.html', context_dict)

def detail(request, patient_id):
    return HttpResponse("You're looking at patient %s." % patient_id)

def thanks(request):
    return HttpResponse("Thanks for adding a patient.")



