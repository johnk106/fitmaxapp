from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'fitmaxapp/index-2.html',{})

def pay(request):
    return render(request,'fitmaxapp/pay.html',{})



def _login(request):
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request,user)
        messages.success(request,'Welcome back {0},we are happy to see you again.'.format(user.first_name))
        return HttpResponseRedirect(reverse('fitMax:index'))
    else:
        messages.warning(request,'Wrong credential combination,please check your credentials and try again.')
        return HttpResponseRedirect(reverse('fitMax:index'))


def sign_up(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    cpass = request.POST['cpassword']

    if password == cpass:
        try:
            user = User.objects.create_user(first_name = fname, last_name = lname, email = email,password = password,username=email)
            user.save()
            login(request,user)
            messages.success(request,'Congratulations {0},You have been successfully registered'.format(fname))
            return HttpResponseRedirect(reverse('fitMax:index'))
        except:
            messages.warning(request,'That username is already taken,please choose another name.')
            return HttpResponseRedirect(reverse('fitMax:index'))
    else:
        messages.warning(request,'Passwords do not match,sign up failed')
        return HttpResponseRedirect(reverse('fitMax:index'))
        
def logout_view(request):
    messages.warning(request,'You have been successfully logged out.')
    logout(request)
    return HttpResponseRedirect(reverse('fitMax:index'))

def required(request):
    messages.warning(request,'Please log in to access this feature')
    return HttpResponseRedirect(reverse('fitMax:index'))