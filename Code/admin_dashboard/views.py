from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from registration.models import CustomUser
from accommodation.models import Accommodation
from django.views import View
from Code.settings import DEFAULT_FROM_EMAIL


class AdminUserDashboard(ListView):
    template_name = 'admin_dashboard/admin_dashboard_users.html'
    model = CustomUser


class AdminAccommodationDashboard(ListView):
    template_name = 'admin_dashboard/admin_dashboard_accommodations.html'
    model = Accommodation


class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        user_pk = kwargs['pk']
        user = get_object_or_404(CustomUser, pk=user_pk)
        send_mail(
            'حذف حساب کاربری مکان',
            'حساب کاربری مکان شما حذف شده است.',
            DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        user.delete()
        return redirect('/admin_dashboard/users')


class AuthenticateAccommodation(View):
    def get(self, request, *args, **kwargs):
        acc_pk = kwargs['pk']
        acc = get_object_or_404(Accommodation, pk=acc_pk)
        acc.is_authenticated = True
        acc.save()
        send_mail(
            'تایید محل اقامت',
            'محل اقامت شما تایید شده است.',
            DEFAULT_FROM_EMAIL,
            [acc.email],
            fail_silently=False,
        )
        return redirect('/admin_dashboard/accommodations')
