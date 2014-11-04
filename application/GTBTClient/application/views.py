# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
def overview(request):
    return render_to_response('application/overview.html',{})

def entity(request):
    return render_to_response('application/Entity-Viewer.html',{})

def search(request):
    return render_to_response('application/search.html',{})

def system(request):
    return render_to_response('application/system.html',{})