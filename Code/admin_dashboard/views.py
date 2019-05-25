from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from registration.models import CustomUser
from accommodation.models import Accommodation
from django.views import View


class AdminUserDashboard(ListView):
    template_name = 'admin_dashboard_users.html'
    model = CustomUser


class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        user_pk = kwargs['pk']
        user = get_object_or_404(CustomUser, pk=user_pk)
        user.delete()
        return redirect('/admin_dashboard')


class DeleteAccommodation(View):
    def get(self, request, *args, **kwargs):
        acc_pk = kwargs['pk']
        acc = get_object_or_404(Accommodation, pk=acc_pk)
        acc.delete()
        return redirect('/admin_dashboard')
