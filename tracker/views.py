from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello and welcome to the Tracker.")

def detail(request, patient_id):
    return HttpResponse("You're looking at patient %s." % patient_id)

