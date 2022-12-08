from django.urls import path
from .views import *


app_name = 'store'
urlpatterns = [
    path('',Home,name='home'),
    path('about/',About,name='about'),
    path('cart/',Cart,name='cart'),
    path('prodDetails/',ProductDetails,name='product-details'),
    path('sucess/',PaymentSucess,name='Sucess'),
    path('fail/',PaymentFailed,name='Failed'),
    path('pay-direct/',PaymentDirection,name='pay-direct'),
]
