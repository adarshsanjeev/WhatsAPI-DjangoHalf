from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.widgets import HiddenInput
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserForm

# import webwhatsapp

@login_required(login_url="/WhatsAPI/login")
def index(request):
    return render(request, "index.html", {})

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
    
