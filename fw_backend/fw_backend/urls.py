"""
URL configuration for fw_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # links up database to admin page

    # this is where all the vehicle stuff happens (checklist, anpr, gargage)
    path('vehicle/', include('vehicle_lookup.urls')),
    # this is where the user stuff happens (signup, login logout)
    path('user/', include('login_signup.urls')),
    #  for the frontend app built into django so i can deploy
    path('', include('frontend.urls')),

]
