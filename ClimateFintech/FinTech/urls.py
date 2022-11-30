from django.urls import path
from .views import *

app_name = 'fintech'

urlpatterns = [
    path('',About,name='about'),
]
