from django.urls import path
from .views import (usersignup,userdel,userlogin,)

urlpatterns = [
    # these are used for the user to sign up log in and delete their account
    path("signup/", usersignup),
    path("login/", userlogin),
    path("del/", userdel),
]
