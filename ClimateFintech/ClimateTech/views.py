from django.shortcuts import render

# Create your views here.
app_name = 'climatetech'

def About(request):
    return render(request,'about_climate.html')