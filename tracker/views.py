from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect

from tracker.models import Step, StepOutcome, NextStepCondition, FlagCondition, COMPARATOR_CHOICES, TRUE, FALSE
from tracker.models import Patient, PatientStep, PatientOutcome, PatientForm, PatientOutcomeForm

from django.utils import timezone

from django.forms.formsets import formset_factory

def evaluate_condition(value, comparison, cmpvalue):
    if comparison == '<':
        if value < cmpvalue:
            return True
    elif comparison == '<=':
        if value <= cmpvalue:
            return True
    elif comparison == '==':
        if value == cmpvalue:
            return True
    elif comparison == '>':
        if value > cmpvalue:
            return True
    elif comparison == '>=':
        if value >= cmpvalue:
            return True
    

    return False

def everything_tracker(request):
    context_dict = {}
    PatientOutcomeFormSet = formset_factory(PatientOutcomeForm,
                                            extra=0)
    AddPatientform = PatientForm(initial={'timeIn': timezone.now()}) #!!!
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

        else:
            patient_objects = Patient.objects.all().order_by('-timeIn')
            for p in patient_objects:
                if(('Patient Outcome-%s' % p.pk) in request.POST ):
                    formset = PatientOutcomeFormSet(request.POST, prefix=unicode(p.pk))
                    if formset.is_valid():
                        for form in formset.forms:
                            if not PatientOutcome.objects.filter(patient=form.cleaned_data['patient'],
                                                               stepOutcome=form.cleaned_data['stepOutcome']
                                                                 ).exists() :
                                new_PO = PatientOutcome.objects.create(patient=form.cleaned_data['patient'],
                                                               stepOutcome=form.cleaned_data['stepOutcome'],
                                                               value=form.cleaned_data['value']
                                                               )
                        current_step = p.patientstep_set.get(current=True)
                        if current_step.step == Step.objects.order_by('-number')[0]:
                            # Maybe need to save the patient object to permanent records here?
                            # Just need to remove the patient from the display...
                            p.delete()
                            break
                        next_step_conditions = current_step.step.nextstepcondition_set.all().order_by('priority')
                        next_step = None
                        for next_step_condition in next_step_conditions:
                            if next_step_condition.dependsOnStepNotDone:
                                step_not_done = next_step_condition.stepNotDone
                                try:
                                    done = p.patientstep_set.get(step=step_not_done)
                                except PatientStep.DoesNotExist:
                                    next_step = next_step_condition.nextStep
                                    break
                                
                            elif next_step_condition.dependsOnOutcome:
                                conditional_outcome = next_step_condition.conditionalOutcome
                                PO = p.patientoutcome_set.get(stepOutcome=conditional_outcome)
                                #PatientOutcome.objects.get(stepOutcome=conditional_outcome, patient=p)
                                cmp1 = next_step_condition.comparator1
                                value1 = next_step_condition.valueToCompare1
                                cmp2 = next_step_condition.comparator2
                                value2 = next_step_condition.valueToCompare2
                                if PO and cmp1 and cmp2 and value1 and value2:
                                    if evaluate_condition(PO.value, cmp1, value1) and evaluate_condition(PO.value, cmp2, value2):
                                        next_step = next_step_condition.nextStep
                                        break
                                elif PO and cmp1 and value1:
                                    if evaluate_condition(PO.value, cmp1, value1):
                                        next_step = next_step_condition.nextStep
                                        break
                                elif PO and cmp2 and value2:
                                    if evaluate_condition(PO.value, cmp2, value2):
                                        next_step = next_step_condition.nextStep
                                        break
                                elif PO and cmp1:
                                    if cmp1 == TRUE:
                                        if PO.value == TRUE:
                                            next_step = next_step_condition.nextStep
                                            break
                                elif PO and cmp2:
                                    if cmp2 == TRUE:
                                        if PO.value == TRUE:
                                            next_step = next_step_condition.nextStep
                                            break

                            elif not next_step_condition.dependsOnStepNotDone and not next_step_condition.dependsOnOutcome:
                                next_step = next_step_condition.nextStep
                                break
                            
                        if next_step:
                            PatientStep.objects.filter(last=True, patient=p).update(last=False)
                            PatientStep.objects.filter(current=True, patient=p).update(current=False, last=True)
                            p_step = PatientStep(step=next_step, patient=p,
                                       current=True, start=timezone.now())
                            p_step.save()
                                

                            
                        return HttpResponseRedirect(reverse('everything_tracker'))
                    else:
                        break                                                           
        
    else:
        pass
    
    # Can order these patients in ascending or descending order of arrival    
    patient_objects = Patient.objects.all().order_by('-timeIn')
    patient_list = []
    for p in patient_objects:
        formset = []
        button_display = "Submit"
        
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

            if current_step.step == Step.objects.order_by('-number')[0]:
                button_display = "Delete Patient"
            elif not step_outcomes.exists():
                button_display = "Next Step"
                
            dict_list = []
            for step_outcome in step_outcomes:
                dict_list.append({'patient': p, 'stepOutcome': step_outcome})
            formset = PatientOutcomeFormSet(initial=dict_list,
                                            prefix=unicode(p.pk))
            
                
        except PatientStep.DoesNotExist:
            #Could raise an error here, or just display None as well.
            #Either way this shouldn't happen.
            current_step = 'None'
        except PatientStep.MultipleObjectsReturned:
            current_step = 'None'
            # What do we want to do here?

        
                
            
        t = (p, last_step, current_step, formset, button_display)
        patient_list.append(t)
    
        
    context_dict['AddPatientform'] = AddPatientform
    context_dict['patient_list'] = patient_list
    return render(request, 'tracker/CSSTracker.html', context_dict)

def detail(request, patient_id):
    return HttpResponse("You're looking at patient %s." % patient_id)

def thanks(request):
    return HttpResponse("Thanks for adding a patient.")



