from django.urls import path
from .views import *


app_name = 'blogs'
urlpatterns = [
    path('',Home,name='home'),
    path('create-post/',CreateBlog,name='create-post'),
    path('blog-display/<str:search>',BlogDisplay,name='blog-display'),
]
