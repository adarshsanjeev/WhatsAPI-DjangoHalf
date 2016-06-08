from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserForm
from django.conf import settings
from django import forms

from WhatsAPIDjango.WhatsAPI.webwhatsapp import WhatsAPIDriver
from time import sleep

Driver_Dict = {}

class MessageForm(forms.Form):
    contact_name = forms.CharField(max_length=100)
    message = forms.CharField(max_length=500)

@login_required
def index(request):
    message = None
    unread = None
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
        except Exception:
            return HttpResponseServerError("Server Error, try again later or contact admin")
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
        unread = user_driver.view_unread()

        return render(request, "index.html", {'form':form, 'message':message, 'unread':unread})

@login_required
def get_unread(request):
    user_driver = Driver_Dict.get(request.user)
    if user_driver is None:
        return Http404("You are not logged in to get messages")
    else:
        messages = user_driver.update_unread()
        if messages == []:
            return HttpResponse("No new messages")
        return HttpResponse(str(messages))
   
def user_register(request):
    if request.POST:
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect('/')
    else:
        user_form = UserForm()
    return render(request, 'registration/register.html', {'user_form':user_form})
    
def redirect(request):
    return HttpResponseRedirect('/')
