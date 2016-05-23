from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.forms.widgets import HiddenInput
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserForm
from django.conf import settings
from django import forms

from WhatsAPI.webwhatsapp import WhatsAPIDriver
from time import sleep

Driver_Dict = {}
# '.spinner-container'
class MessageForm(forms.Form):
    contact_name = forms.CharField(max_length=100)
    message = forms.CharField(max_length=500)

@login_required(login_url="/WhatsAPI/login/")
def index(request):
    message = None

    user_driver = Driver_Dict.get(request.user)
    if user_driver is None:
        try:
            Driver_Dict[request.user] = WhatsAPIDriver(request.user.username)
            user_driver = Driver_Dict[request.user]
            sleep(1)
        except:
            Driver_Dict[request.user] = None
            return HttpResponseServerError("Server Error: Could not create a new driver")
    if "Use WhatsApp on your phone to scan the code" in user_driver.driver.page_source:
        try:
            user_driver.firstrun()
            filename = request.user.username+".png"
            return render(request, 'index.html', {'filename':filename})
        except Exception as e:
            return HttpResponseServerError("Server Error, try again later %s" %(str(e)))
    else:
        if request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                contact = form.cleaned_data['contact_name']
                message = form.cleaned_data['message']
                val = user_driver.send_message(contact, message)
                if val is True:
                    message = "Message sent"
                    form = MessageForm()
                elif val is False:
                    message = "Contact not found"
                else:
                    message = str(val)
        else:
            form = MessageForm()
        return render(request, "index.html", {'form':form, 'message':message})

@login_required(login_url="/WhatsAPI/login/")
def get_unread(request):
    user_driver = Driver_Dict.get(request.user)
    if user_driver is None:
        return Http404("You are not logged in to get messages")
    else:
        messages = user_driver.update_unread()
        if messages == []:
            return HttpResponse("No new messages")
        return HttpResponse(str(messages))

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
    return HttpResponseRedirect("/WhatsAPI/login")
    
