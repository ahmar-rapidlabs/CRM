from django.shortcuts import render
from djangohttp import HttpResponse
# Create your views here.
def views(request):
    return HttpResponse("hello")