from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from khayyam import JalaliDate

from payment.models import Transaction
from registration.models import CustomUser
from accommodation.models import Accommodation
from django.views import View
from Code.settings import DEFAULT_FROM_EMAIL
from reservation.models import Reservation
from search_index.filters import AccommodationFilter
from .decorators import user_is_superuser

decorators = [login_required, user_is_superuser]


@method_decorator(decorators, name='dispatch')
class AdminDashboard(View):
    template_name = 'admin_dashboard/admin_dashboard.html'

    def get(self, request, *args, **kwargs):
        reservations = Reservation.objects.annotate(month=TruncMonth('transaction__creation_date')).values(
            'month').annotate(count=Count('id'))
        reservations_month = list(
            set([JalaliDate(x).strftime('%B') for x in list(reservations.values_list('month', flat=True))]))
        reservations_count = list(reservations.values_list('count', flat=True))
        earnings = [[datetime.combine(x.creation_date, datetime.min.time()).timestamp() * 1000, x.total_price * 0.05]
                    for x in
                    Transaction.objects.all()]
        all_reservations_count = Reservation.objects.count()
        all_cancelled_reservations_count = Reservation.objects.filter(is_canceled=True).count()
        return render(request, self.template_name,
                      {'earnings': earnings, 'reserve_month': reservations_month,
                       'reserve_count': reservations_count, 'all_count': all_reservations_count,
                       'all_cancelled_count': all_cancelled_reservations_count})


@method_decorator(decorators, name='dispatch')
class AdminUserDashboard(ListView):
    template_name = 'admin_dashboard/admin_dashboard_users.html'
    model = CustomUser

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminUserDashboard, self).get_context_data(**kwargs)
        users = self.get_queryset().annotate(month=TruncMonth('date_joined')).values('month').annotate(
            count=Count('id'))
        date_joined = list(
            set([JalaliDate(x).strftime('%B') for x in list(users.values_list('month', flat=True))]))
        user_count = list(users.values_list('count', flat=True))
        context['date_joined'] = date_joined
        context['user_count'] = user_count
        return context


@method_decorator(decorators, name='dispatch')
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


@method_decorator(decorators, name='dispatch')
class AdminAccommodationStatsDashboard(View):
    template_name = 'admin_dashboard/admin_dashboard_accommodations_stats.html'

    def get(self, request, *args, **kwargs):
        hotels = Accommodation.objects.filter(accommodation_type='هتل').count()
        motels = Accommodation.objects.filter(accommodation_type='اقامتگاه').count()
        houses = Accommodation.objects.filter(accommodation_type='منزل شخصی').count()
        return render(request, self.template_name, {'hotels': hotels, 'motels': motels, 'houses': houses})


@method_decorator(decorators, name='dispatch')
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


@method_decorator(decorators, name='dispatch')
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
