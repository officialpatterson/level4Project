# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
def overview(request):
    return render_to_response('application/overview.html',{})

def entity(request):
    return render_to_response('application/Entity-Viewer.html',{})

def search(request):
    response = "search-page"
    return HttpResponse(response)

def system(request):
    response = "system-page, change classifiers, take samples to crowdsource etc."
    return HttpResponse(response)