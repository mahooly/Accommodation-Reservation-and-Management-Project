import json
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from khayyam import JalaliDate

from payment.models import Transaction
from registration.models import CustomUser
from accommodation.models import Accommodation, RoomInfo
from django.views import View
from Code.settings import DEFAULT_FROM_EMAIL
from reservation.filters import ReservationFilter
from reservation.models import Reservation
from search_index.filters import AccommodationFilter
from .decorators import user_is_superuser

decorators = [login_required, user_is_superuser]


@method_decorator(decorators, name='dispatch')
class AdminDashboard(View):
    template_name = 'admin_dashboard/admin_dashboard.html'

    def get(self, request, *args, **kwargs):
        reservations = Reservation.objects.get_count_by_month()
        cancelled_reservations = Reservation.objects.get_cancelled_count_by_month()
        reservations_month, reservations_count = self.get_reservation_chart_data(reservations)
        _, cancelled_reservations_count = self.get_reservation_chart_data(cancelled_reservations)
        earnings = self.get_earning_chart_data()
        all_reservations_count = Reservation.objects.count()
        all_cancelled_reservations_count = Reservation.objects.filter(is_canceled=True).count()
        return render(request, self.template_name,
                      {'earnings': earnings, 'reserve_month': reservations_month,
                       'reserve_count': reservations_count, 'all_count': all_reservations_count,
                       'all_cancelled_count': all_cancelled_reservations_count,
                       'cancelled_reserve_count': cancelled_reservations_count})

    def get_daily_earnings(self):
        all_transactions = Transaction.objects.all()
        daily_earn = {}
        for transaction in all_transactions:
            if transaction.creation_date in daily_earn:
                daily_earn[transaction.creation_date] += transaction.total_price
            else:
                daily_earn[transaction.creation_date] = transaction.total_price
        return daily_earn

    def get_earning_chart_data(self):
        daily_earnings = self.get_daily_earnings()
        earnings = [[datetime.combine(key, datetime.min.time()).timestamp() * 1000, daily_earnings[key] * 0.05]
                    for key in
                    daily_earnings.keys()]
        return earnings

    def get_reservation_chart_data(self, reservations):
        reservations_month = list(
            set([JalaliDate(x).strftime('%B') for x in list(reservations.values_list('month', flat=True))]))
        reservations_count = [1] * len(reservations_month)
        month = None
        i = -1
        for res in reservations:
            if res['month'] == month:
                reservations_count[i] += 1
            else:
                month = res['month']
                i += 1
        return reservations_month, reservations_count


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
        location_filtered = Accommodation.objects.values('city').annotate(count=Count('id'))
        hotels, motels, houses, inactive_hotels, inactive_motels, inactive_houses = self.get_accommodation_chart_data()
        data, series = self.get_empty_rooms_chart_data()
        return render(request, self.template_name,
                      {'hotels': hotels.count(), 'motels': motels.count(), 'houses': houses.count(),
                       'inactive_hotels': inactive_hotels,
                       'inactive_motels': inactive_motels, 'inactive_houses': inactive_houses,
                       'location_filtered': location_filtered, 'data': data, 'series': series})

    def get_empty_rooms_chart_data(self):
        infos = RoomInfo.objects.get_available_room_infos(datetime.today(), datetime.today())
        empty_city = infos.values('room__accommodation__city').annotate(count=Count('id'))
        data = []
        series = []
        for info in empty_city:
            drill_down_data = []
            data.append({'name': info['room__accommodation__city'], 'y': info['count'],
                         'drilldown': info['room__accommodation__city']})
            drill_down = infos.filter(room__accommodation__city=info['room__accommodation__city']).values(
                'room__accommodation__title').annotate(count=Count('id'))
            for d in drill_down:
                drill_down_data.append([d['room__accommodation__title'], d['count']])
            series.append({'name': info['room__accommodation__city'], 'id': info['room__accommodation__city'],
                           'data': drill_down_data})
        data = json.dumps(data)
        series = json.dumps(series)
        return data, series

    def get_accommodation_chart_data(self):
        hotels = Accommodation.objects.get_hotels()
        motels = Accommodation.objects.get_motels()
        houses = Accommodation.objects.get_houses()
        inactive_hotels = hotels.filter(is_inactive=True).count()
        inactive_motels = motels.filter(is_inactive=True).count()
        inactive_houses = houses.filter(is_inactive=True).count()
        return hotels, motels, houses, inactive_hotels, inactive_motels, inactive_houses


class AdminReservationsDashboard(ListView):
    template_name = 'admin_dashboard/admin_dashboard_reservations.html'
    paginate_by = 10

    def get_queryset(self):
        reserve_list = Reservation.objects.all()
        return ReservationFilter(self.request.GET, reserve_list).qs


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
