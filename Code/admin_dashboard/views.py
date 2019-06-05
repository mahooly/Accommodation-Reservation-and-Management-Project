from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from registration.models import CustomUser
from accommodation.models import Accommodation
from django.views import View
from Code.settings import DEFAULT_FROM_EMAIL
from search_index.filters import AccommodationFilter


class AdminUserDashboard(ListView):
    template_name = 'admin_dashboard/admin_dashboard_users.html'
    model = CustomUser


class AdminAccommodationDashboard(ListView):
    template_name = 'admin_dashboard/admin_dashboard_accommodations.html'
    model = Accommodation

    def get_queryset(self):
        auth = self.request.GET.get('is_authenticated', '')
        q = Accommodation.objects.all()
        if auth:
            if auth == 'True':
                q = q.filter(is_authenticated=True)
            else:
                q = q.filter(is_authenticated=False)
        f = AccommodationFilter(self.request.GET, queryset=q)
        return f.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.request.GET.get('type', '')
        context['province'] = self.request.GET.get('province', '')
        context['city'] = self.request.GET.get('city', '')
        context['is_authenticated'] = self.request.GET.get('is_authenticated', '')
        return context


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
        messages.success(request, 'حساب کاربری با موفقیت حذف شد.')
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
        messages.success(request, 'اقامتگاه با موفقیت تایید شد.')
        return redirect('/admin_dashboard/accommodations')
