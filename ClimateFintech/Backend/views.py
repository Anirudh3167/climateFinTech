from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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

def Login(request):
  if request.method == 'POST':
    if (request.POST['form-type'] == 'login'):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        new_user = authenticate(username=username,password=password)
        if new_user is not None:
          login(request,new_user)
          return redirect('index')
    if (request.POST['form-type'] == 'register'):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        new_user = User.objects.create_user(username=username,email=email,password=password)
        new_user.save()
        login(request,new_user)
        return redirect('index')
  return render(request,'login.html')

def Logout(request):
  logout(request)
  return redirect('index')