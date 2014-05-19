from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect

from tracker.models import Step, StepOutcome, NextStepCondition, FlagCondition
from tracker.models import Patient, PatientStep, PatientOutcome, PatientForm, PatientOutcomeForm

from django.utils import timezone

from django.forms.formsets import formset_factory


def everything_tracker(request):
    context_dict = {}
    PatientOutcomeFormSet = formset_factory(PatientOutcomeForm,
                                            extra=0)
    
    if request.method == 'POST': # If a form has been submitted.
        
        if 'Add Patient' in request.POST:
            AddPatientform = PatientForm(request.POST) # A PatientForm bound to the POST data.
            if AddPatientform.is_valid(): # If validation rules pass
                new_p = Patient.objects.create(name=AddPatientform.cleaned_data['name'],
                                       dob=AddPatientform.cleaned_data['dob'],
                                       timeIn=AddPatientform.cleaned_data['timeIn'] )

                #Associate a new PatientStep with the newly created patient, and start it on the
                # first step as defined in the Admin page.
                first_step = Step.objects.get(number=1)
                p_step = PatientStep(step=first_step, patient=new_p,
                                       current=True, start=timezone.now())
                p_step.save()
        
                return HttpResponseRedirect(reverse('everything_tracker')) # Redirect to the same view
            else:
                pass #Just let the bound form with invalid data go to the very end, to display errors.
            
        elif 'Patient Outcome' in request.POST:
            print request.POST
            patient_objects = Patient.objects.all().order_by('-timeIn')
            for p in patient_objects:
                formset = PatientOutcomeFormSet(request.POST, prefix=unicode(p))
                if formset.is_valid():
                    for form in formset.forms:
                        new_PO = PatientOutcome.objects.create(patient=form.cleaned_data['patient'],
                                                               stepOutcome=form.cleaned_data['stepOutcome'],
                                                               value=form.cleaned_data['value']
                                                               )
                    #here set the patient's current step to the new thingy based
                    # off of nextstepconditions.
                    return HttpResponseRedirect(reverse('everything_tracker'))
                        
                                                               

        
    else:
        AddPatientform = PatientForm(initial={'timeIn': timezone.now()}) # Blank form to add a new patient
            
    # Can order these patients in ascending or descending order of arrival    
    patient_objects = Patient.objects.all().order_by('-timeIn')
    patient_list = []
    for p in patient_objects:
        formset = []
        
        try:
            last_step = p.patientstep_set.get(last=True)
        except PatientStep.DoesNotExist:
            last_step = "None"
        except PatientStep.MultipleObjectsReturned:
            last_step = "None"
            #Raise some error that doesn't crash everything?

            
        try:
            current_step = p.patientstep_set.get(current=True)
            
            step_outcomes = current_step.step.stepoutcome_set.all()
            dict_list = []
            for step_outcome in step_outcomes:
                dict_list.append({'patient': p, 'stepOutcome': step_outcome})
            formset = PatientOutcomeFormSet(initial=dict_list,
                                            prefix=unicode(p))
            
                
        except PatientStep.DoesNotExist:
            #Could raise an error here, or just display None as well.
            #Either way this shouldn't happen.
            current_step = 'None'
        except PatientStep.MultipleObjectsReturned:
            current_step = 'None'
            # What do we want to do here?

        
                
            
        t = (p, last_step, current_step, formset)
        patient_list.append(t)
    
        
    context_dict['AddPatientform'] = AddPatientform
    context_dict['patient_list'] = patient_list
    return render(request, 'tracker/CSSTracker.html', context_dict)

def detail(request, patient_id):
    return HttpResponse("You're looking at patient %s." % patient_id)

def thanks(request):
    return HttpResponse("Thanks for adding a patient.")



