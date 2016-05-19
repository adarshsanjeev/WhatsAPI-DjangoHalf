from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.widgets import HiddenInput
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserForm
from django.conf import settings

from WhatsAPI.webwhatsapp import WhatsAPIDriver
from time import sleep

Driver_Dict = {}

@login_required(login_url="/WhatsAPI/login/")
def index(request):
    user_driver = Driver_Dict.get(request.user)
    if user_driver is None:
        try:
            Driver_Dict[request.user] = WhatsAPIDriver()
            user_driver = Driver_Dict[request.user]
            user_driver.username = request.user.username
            sleep(1)
            user_driver.firstrun()
            filename = request.user.username+".png"
            return render(request, 'index.html', {'filename':filename})
        except:
            Driver_Dict[request.user] = None
            return HttpResponse("Server Error, try again later")
    else:
        user_driver.send_message("Mukul", "Test Message from django, sup")
    return HttpResponse("SUCCESS")
    # return render(request, "index.html", {})

def user_login(request):
    form_errors = None
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/WhatsAPI')
        else:
            form_errors = "Username or password is incorrect"
    return render(request, 'login.html', {'form_errors':form_errors}) 
   
def user_register(request):
    if request.POST:
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            return HttpResponseRedirect('/WhatsAPI/login')
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'user_form':user_form})

@login_required(login_url="/WhatsAPI/login")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/WhatsAPI")
    
