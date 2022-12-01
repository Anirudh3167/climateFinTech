from django.shortcuts import render

# Create your views here.

def Home(request):
    return render(request,'home_store.html')

def About(request):
    return render(request,'about_climate.html')