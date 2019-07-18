import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView

from accommodation.decorators import user_same_as_accommodation_user
from registration.decorators import user_is_host, user_is_confirmed
from reservation.filters import ReservationFilter
from .forms import MakeReservationForm
from .models import Reservation
from payment.models import Transaction
from accommodation.models import Room, RoomInfo, Accommodation
from Code.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from utils.utils import convert_string_to_date


@method_decorator([login_required, user_is_confirmed, user_is_host, user_same_as_accommodation_user], name='dispatch')
class AccommodationReservationList(ListView):
    template_name = "reservation/accommodation_reservation.html"
    paginate_by = 10

    def get_queryset(self):
        reserve_list = Reservation.objects.filter(roominfo__room__accommodation_id=self.kwargs['pk'])
        return ReservationFilter(self.request.GET, reserve_list).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        acc = self.get_accommodation()
        context['accommodation'] = acc
        return context

    def get_accommodation(self):
        pk = self.kwargs.get('pk')
        return Accommodation.objects.get(pk=pk)


@method_decorator([login_required, user_is_confirmed], name='dispatch')
class UserReservationList(ListView):
    template_name = "reservation/user-reservations.html"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        reserve_list = Reservation.objects.filter(reserver=user)
        return ReservationFilter(self.request.GET, reserve_list).qs


@method_decorator([login_required, user_is_confirmed], name='dispatch')
class MakeReservation(View):

    def post(self, request, *args, **kwargs):
        form = MakeReservationForm(request.POST)
        room = get_object_or_404(Room, pk=kwargs['rid'])
        if form.is_valid():
            how_many = int(form.cleaned_data.get('how_many'))
            check_in = convert_string_to_date(form.cleaned_data.get('check_in'))
            check_out = convert_string_to_date(form.cleaned_data.get('check_out'))
            available_room_infos = self.get_available_room_infos(room, check_in, check_out)
            if len(available_room_infos) < how_many:
                messages.error(request,
                               'در رزرو کردن اتاق مشکلی پیش آمده است. لطفاً دوباره تلاش کنید. به این تعداد اتاق خالی وجود ندارد.')
                return redirect(reverse('accommodation_detail', kwargs={'pk': room.accommodation.pk}))
            count = 0
            reserve = Reservation.objects.create(reserver=request.user, check_in=check_in,
                                                 check_out=check_out)
            for room_info in available_room_infos:
                if count < how_many:
                    reserve.roominfo.add(room_info)
                    count += 1
            self.send_mail_to_host(room, reserve, request.user, form.cleaned_data['check_in'],
                                   form.cleaned_data['check_out'])
            messages.success(request, 'رزرو شما با موفقیت ثبت شد.')
            context = {'rid': reserve.pk}
            return redirect(reverse('payment', kwargs={'resid': reserve.pk}), context)
        else:
            messages.error(request, 'در رزرو کردن اتاق مشکلی پیش آمده است. لطفاً دوباره تلاش کنید.')
            return redirect(reverse('accommodation_detail', kwargs={'pk': room.accommodation.pk}))

    def get_available_room_infos(self, room, check_in, check_out):
        available_room_infos = RoomInfo.objects.get_available_room_infos(check_in, check_out)
        available_room_infos = available_room_infos.filter(room=room)
        return available_room_infos

    def send_mail_to_host(self, room, reserve, user, check_in, check_out):
        email_text = 'محل اقامت شما به آدرس {} توسط {} {} برای تاریخ {} تا {} رزرو شده است.' \
                     ' مقدار {} برای شما در تاریخ شروع واریز خواهد شد.'.format(
            room.accommodation.address, user.first_name, user.last_name, check_in, check_out,
            str(reserve.total_price * 0.95))
        send_mail(
            'رزرو محل اقامت',
            email_text,
            DEFAULT_FROM_EMAIL,
            [room.accommodation.owner.user.email],
            fail_silently=True,
        )


@method_decorator([login_required, user_is_confirmed], name='dispatch')
class CancelReservation(View):

    def get(self, request, *args, **kwargs):
        res_id = kwargs['resid']
        reservation = get_object_or_404(Reservation, id=res_id)
        reservation.is_canceled = True
        reservation.save()
        self.send_mail_to_host(reservation)
        self.send_mail_to_guest(reservation)
        self.create_opposite_transaction(reservation)
        messages.success(request, 'لغو رزرو با موفقیت انجام شد.')
        return redirect('user_reserve')

    def how_late(self, reservation):
        today = datetime.datetime.now()
        check_in = reservation.check_in
        diff = today - check_in
        return diff.days

    def send_mail_to_host(self, reservation):
        host_email = reservation.roominfo.first().room.accommodation.owner.user.email
        diff = self.how_late(reservation)
        due = 0
        if diff <= 10:
            ekh = 11 - diff
            due += reservation.total_price * ekh * 0.1

        text = 'رزرو با کد {} لغو شده است.'.format(reservation.id)
        if due > 0:
            text += 'مقدار {} به حساب شما واریز خواهد شد.'.format(str(due))
        send_mail(
            'لغو رزرو',
            text,
            DEFAULT_FROM_EMAIL,
            [host_email],
            fail_silently=True,
        )

    def send_mail_to_guest(self, reservation):
        guest_email = reservation.reserver.email
        diff = self.how_late(reservation)
        due = 0
        if diff <= 10:
            ekh = 11 - diff
            due += reservation.total_price * (1 - ekh * 0.1)
        text = 'رزرو با کد {} لغو شده است.'.format(reservation.id)
        if due > 0:
            text += 'مقدار {} به حساب شما واریز خواهد شد.'.format(str(due))
        send_mail(
            'لغو رزرو',
            self.get_guest_email_text,
            DEFAULT_FROM_EMAIL,
            [guest_email],
            fail_silently=True,
        )

    def create_opposite_transaction(self, reservation):
        Transaction.objects.create(is_successful=True, reservation=reservation, coefficient=-1)
