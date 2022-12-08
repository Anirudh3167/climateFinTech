from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.forms.models import model_to_dict
#from django.template import loader

# assigning User as our User model i.e. as User_details
User = get_user_model()

def index(request):
  #template = loader.get_template('index.html')
  context = {'name': 'programmer', 'id':'programming','variable':'ntg'}
  return render(request,'index.html',context)

def Help(request):
  return render(request,'Helpdesk.html')
def FAQ(request):
  return render(request,'FAQ.html')
# def Ankush(request):
#   return render(request,'sample_Ankush.html')
# def AboutFinTech(request):
#   return render(request,'about_fintech.html')
# def AboutClimate(request):
  # return render(request,'about_climate.html')

#@login_required(login_url='Login')
def UserProfile(request,uname=''):
  print(f"UNAME:{uname}")
  if request.user.is_anonymous:
    print("Annonymous User")
    verified = False
    if uname == '':
      return redirect('Login')
  else:
    if uname == '': 
      uname = request.user
    username = request.user
    if uname == str(username):
      verified = True
    else:
      verified = False
    # print(f"VERIFIED:{verified}")
    # print(f"UNAME:{uname},USERNAME:{username}")
  User_det = model_to_dict(User.objects.filter(username=uname).first())
  if User_det is []:
    return render(request,'index.html')
  User_det["verified"] = verified
  # print(User_det)
  return render(request,'userProfile.html',User_det)


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

          #getting the url
          try:
            return redirect(request.GET["next"])
          except:
            return redirect("index")
            
    if (request.POST['form-type'] == 'register'):
        #Basic User details.
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