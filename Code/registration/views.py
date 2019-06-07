from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from .forms import *
from accommodation.models import Accommodation
from .decorators import user_is_host


class RegistrationView(View):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'

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


@method_decorator(login_required, name='dispatch')
class HostRegistration(View):
    form_class = HostForm
    template_name = 'registration/host.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            host = form.save(commit=False)
            host.user = user
            host.save()
            user.is_host = True
            user.save()
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class EditProfile(View):
    template_name = 'registration/changeinfo.html'

    def get(self, request, *args, **kwargs):
        user_form = CustomUserChangeForm(instance=request.user,
                                         initial={'email': request.user.email, 'gender': request.user.gender,
                                                  'image': request.user.image})
        password_form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'user_form': user_form, 'password_form': password_form})

    def post(self, request, *args, **kwargs):
        if 'user_form' in request.POST:
            user_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
            password_form = PasswordChangeForm(request.user)
            if user_form.is_valid():
                user = user_form.save()
                user.save()
                messages.success(request, 'اطلاعات شما با موفقیت ثبت شد.')
        else:
            password_form = PasswordChangeForm(request.user, request.POST)
            user_form = CustomUserChangeForm(instance=request.user,
                                             initial={'email': request.user.email, 'gender': request.user.gender,
                                                      'image': request.user.image})
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'اطلاعات شما با موفقیت ثبت شد.')

        return render(request, self.template_name, {'user_form': user_form, 'password_form': password_form})


@method_decorator([login_required, user_is_host], name='dispatch')
class HostDashboard(ListView):
    template_name = 'registration/host_dashboard.html'

    def get_queryset(self):
        return Accommodation.objects.filter(owner=self.request.user.host)


class ProfileView(DetailView):
    template_name = 'registration/profile.html'
    model = CustomUser
