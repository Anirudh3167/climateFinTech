from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
#from django.template import loader

def index(request):
  #template = loader.get_template('index.html')
  context = {'name': 'programmer', 'id':'programming','variable':'ntg'}
  return render(request,'index.html',context)

def Ankush(request):
  return render(request,'sample_Ankush.html')
def AboutFinTech(request):
  return render(request,'about_fintech.html')
def AboutClimate(request):
  return render(request,'about_climate.html')
def UserProfile(request):
  return render(request,'userProfile.html')


def Abhinav(request):
  return render(request,'sample_Abhinav.html')


def Lakshay(request):
  return render(request,'sample_Lakshay.html')

def handler404(request,exception):
  response = render(request,"404.html")
  response.status_code = 404
  return response