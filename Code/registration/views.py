from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from khayyam import JalaliDate

from registration.tokens import account_activation_token
from .forms import *
from accommodation.models import Accommodation
from .decorators import user_is_host, user_is_confirmed

persian_numbers = '۱۲۳۴۵۶۷۸۹۰'
english_numbers = '1234567890'
trans_num = str.maketrans(persian_numbers, english_numbers)


class RegistrationView(View):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            birth_date = self.convert_string_to_date(form.cleaned_data['birthday'])
            user = form.save(commit=False)
            user.birth_date = birth_date
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            current_site = get_current_site(request)
            subject = 'فعال‌سازی حساب کاربری مکان'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation')

        return render(request, self.template_name, {'form': form})

    def convert_string_to_date(self, date_string):
        split_string = [int(x.translate(trans_num)) for x in date_string.split('/')]
        return JalaliDate(split_string[0], split_string[1], split_string[2]).todate()


class ActivateAccount(View):
    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, kwargs['token']):
            user.is_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, 'حساب کاربری شما با موفقیت تایید شد!')
            return redirect(reverse('user_dashboard', kwargs={'uid': user.pk}))
        else:
            return render(request, 'registration/account_activation_invalid.html')


@method_decorator([login_required, user_is_confirmed], name='dispatch')
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


@method_decorator([login_required, user_is_confirmed], name='dispatch')
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

        password_form = PasswordChangeForm(request.user)
        user_form = CustomUserChangeForm(instance=request.user,
                                         initial={'email': request.user.email, 'gender': request.user.gender,
                                                  'image': request.user.image})

        return render(request, self.template_name, {'user_form': user_form, 'password_form': password_form})


@method_decorator([login_required, user_is_confirmed], name='dispatch')
class HostDashboard(ListView):
    template_name = 'registration/host_dashboard.html'

    def get_queryset(self):
        return Accommodation.objects.filter(owner=self.request.user.host)


class ProfileView(DetailView):
    template_name = 'registration/profile.html'
    model = CustomUser
