from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

badreq = 400
notauthorised =401
created = 201
@api_view(["POST"])
def usersignup(request):
    userdata = request.data

    # ensures all the fields are put in, password in long enough and that they match
    if not userdata.get("username") or not userdata.get("password") or not userdata.get("password2"): return Response({"signuperror": "Username or Password missing"}, status=badreq)
    if len(userdata.get("password")) < 8:return Response({"signuperror": "Password Needs To Be 8 Characters"}, status=badreq)
    if userdata.get("password") != userdata.get("password2"): return Response({"signuperror": "Passwords Do Not Match"}, status=badreq)

    # checks that the username isnt already used
    if User.objects.filter(username=userdata["username"]).exists(): return Response({"signuperror": "Username Exists"}, status=badreq)

    # if all checks are good then make a new user
    newuser = User.objects.create_user(username=userdata["username"], password=userdata["password"],)

    # make the token for the user and give it to the frontend with the linked user
    usertoken = Token.objects.create(user=newuser)
    return Response({ "token": usertoken.key, "username": newuser.username }, status=created)

@api_view(["POST"])
def userlogin(request):
    userdata = request.data

    # check the details are all correct
    correctuser = authenticate(username=userdata.get("username"), password=userdata.get("password"))
    
    if correctuser is not None: # in the case we get a correct user so its a valid login
        token, created = Token.objects.get_or_create(user=correctuser) # make a token if needed 
        return Response({"token": token.key,"username": correctuser.username}) # give the frontend the token and the linked user
    
    return Response({"loginerror": "Username or Password Is Wrong"}, status=notauthorised) # if it didnt pass the check returns a error

@api_view(["DELETE"])
@permission_classes([IsAuthenticated]) # make sure the user is logged in
def userdel(request): # simply delete the user and tell the frontend its deleted
    request.user.delete()
    return Response({"status": "account deleted"})

