from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *


def index(request):
    # TODO: index.html
    print('&' * 100)
    # print(request.user)
    return render(request, 'base.html')


def register(request):
    if request.method == 'POST':
        signupform = CustomUserCreationForm(data=request.POST)

        if signupform.is_valid():
            username = signupform.cleaned_data['username']
            password = signupform.cleaned_data['password1']
            signupform.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        signupform = CustomUserCreationForm()
    return render(request, 'register.html', {'form': signupform})



def becomeHost(request):
    if request.method == 'POST':
        host_form = HostForm(data=request.POST)

        if host_form.is_valid():
            user = request.user
            host = host_form.save(commit=False)
            host.user = user
            host.save()
            return redirect('/')
        else:
            print(host_form.errors)
    else:
       host_form = HostForm()
    return render(request, 'host.html', {'form': host_form})


def updateInformation(request):
    if request.method == 'POST':
        userchange_form = CustomUserChangeForm(data=request.POST, instance=request.user, initial={'email':request.user.email, 'gender':request.user.gender})
        if userchange_form.is_valid():
            print("I am here!")
            print(userchange_form)
            user = userchange_form.save()
            print(user)
            # request.user.set_password(userchange_form.cleaned_data['password'])
            user.save()
            return redirect('/')
        else:
            print("error")
    else:
        userchange_form = CustomUserChangeForm(initial={'email':request.user.email, 'gender':request.user.gender})
    return render(request, 'changeinfo.html' , {'form': userchange_form})