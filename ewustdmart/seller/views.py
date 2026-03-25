from django.shortcuts import render
from django.shortcuts import render, HttpResponse

# Create your views here.
def seller_home(request):
    return HttpResponse("This is seller")