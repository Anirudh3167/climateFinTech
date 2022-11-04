from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
#from django.template import loader

def index(request):
  #template = loader.get_template('index.html')
  context = {'name': 'programmer', 'id':'programming','variable':'ntg'}
  return render(request,'index.html',context)

def Ankush(request):
  return render(request,'sample_Ankush.html')


def Abhinav(request):
  return render(request,'sample_Abhinav.html')


def Lakshay(request):
  return render(request,'sample_Lakshay.html')