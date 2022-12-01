from django.urls import path
from .views import *

app_name = 'store'
urlpatterns = [
    path('',Home,name='home'),
    path('about/',About,name='about'),
]
