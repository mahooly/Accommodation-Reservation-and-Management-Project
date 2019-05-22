from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .forms import *


def index(request):
    # TODO: index.html
    print('&' * 100)
    # print(request.user)
    return render(request, 'base.html')


class RegistrationView(View):
    form_class = CustomUserCreationForm
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


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
        if 'user_form' in request.POST:
            user_form = CustomUserChangeForm(data=request.POST)
            password_form = PasswordChangeForm(request.user)
            if user_form.is_valid():
                user = user_form.save()
                user.save()
                return redirect('/')
        else:
            password_form = PasswordChangeForm(request.user, request.POST)
            user_form = CustomUserChangeForm()
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
    else:
        user_form = CustomUserChangeForm()
        password_form = PasswordChangeForm(request.user)

    return render(request, 'changeinfo.html', {'user_form': user_form, 'password_form': password_form})
