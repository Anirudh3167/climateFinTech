from django.shortcuts import render

# Create your views here.
app_name = 'climatetech'

def Home(request):
    return render(request,'home_climate.html')

def About(request):
    return render(request,'about_climate.html')

