"""ClimateFintech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from Backend.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #API URLS
    path('api/',include('api.urls')),

    #ClimateFinTech URLS
    path('',index,name='index'),
    path('login/',Login,name='Login'),
    path('logout/',Logout,name='Logout'),

    #ClimateTech URLS
    path('climatetech/',include('ClimateTech.urls',namespace='climatetech')),
    #FinTech URLS
    path('fintech/',include('FinTech.urls',namespace='fintech')),
    #Store URLS
    path('store/',include('Store.urls',namespace='store')),

    # path('AboutFinTech/',AboutFinTech,name='AboutFinTech'),
    # path('AboutClimate/',AboutClimate,name='AboutClimate'),
    path('UserProfile/',UserProfile,name='UserProfile'),

    #TEST URLS
    #path('Ankush/',Ankush),
    path('Abhinav',Abhinav),
    path('Lakshay',Lakshay),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
