from django.shortcuts import render

# Create your views here.

def Home(request):
    return render(request,'home_fintech.html')

def About(request):
    return render(request,'about_fintech.html')