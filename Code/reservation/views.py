import datetime
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MakeReservationForm, PaymentForm
from .models import Reservation, Transaction
from accommodation.models import Room, RoomInfo
from Code.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail


class ReservationDetail(View):
    template_name = "reservation/accommodation_reservation.html"

    def get(self, request):
        return render(request, self.template_name)


class AllReservations(View):
    template_name = "reservation/all-reservations.html"

    def get(self, request):
        return render(request, self.template_name)


class MakeReservation(View):
    format = '%m/%d/%Y'

    def convert_string_to_date(self, date_string):
        return datetime.datetime.strptime(date_string, self.format)

    def get_available_room_infos(self, room, check_in, check_out):

        availableRoomInfos1 = RoomInfo.objects.all().exclude(
            Q(reservation__check_in__range=(check_in, check_out - datetime.timedelta(days=1))),
            Q(reservation__is_canceled=False))
        availableRoomInfos2 = availableRoomInfos1.exclude(
            Q(reservation__check_out__range=(check_in + datetime.timedelta(days=1), check_out)),
            Q(reservation__is_canceled=False))
        availableRoomInfos = availableRoomInfos2.filter(out_of_service=False, room=room)
        return availableRoomInfos

    def post(self, request, *args, **kwargs):
        form = MakeReservationForm(request.POST)
        room_id = kwargs['rid']
        room = get_object_or_404(Room, pk=room_id)
        print(form)
        if form.is_valid():
            how_many = int(form.cleaned_data.get('how_many'))
            check_in = self.convert_string_to_date(form.cleaned_data.get('check_in'))
            check_out = self.convert_string_to_date(form.cleaned_data.get('check_out'))
            available_room_infos = self.get_available_room_infos(room, check_in, check_out)
            count = 0
            reserve = Reservation.objects.create(reserver=request.user, check_in=check_in,
                                                 check_out=check_out)
            reserve.save()
            email_text = 'محل اقامت شما به آدرس '
            email_text += room.accommodation.address
            email_text += ' توسط '
            email_text += request.user.first_name
            email_text += request.user.last_name
            email_text += ' برای تاریخ '
            email_text += check_in
            email_text += ' تا '
            email_text += check_out
            email_text += ' رزرو شده است. مقدار '
            email_text += str(reserve.total_price * 0.95)
            email_text += ' برای شما در تاریخ شروع واریز خواهد شد.'
            send_mail(
            'رزرو محل اقامت',
            email_text,
            DEFAULT_FROM_EMAIL,
            [acc.email],
            fail_silently=False,
            )
            for room_info in available_room_infos:
                if count < how_many:
                    reserve.roominfo.add(room_info)
                    count += 1
            messages.success(request, 'رزرو شما با موفقیت ثبت شد.')
            url = '/payment/' + str(reserve.pk)
            context = {'rid': reserve.pk}
            return redirect(url, context)
        else:
            messages.error(request, 'در رزرو کردن اتاق مشکلی پیش آمده است. لطفاً دوباره تلاش کنید.')
            accommodation_id = room.accommodation.pk
            url = '/accommodation/' + str(accommodation_id)
            return redirect(url)


class CancelReservation(View):
    def how_late(self, reservation):
        today = datetime.datetime.now()
        check_in = reservation.check_in
        diff = today - check_in
        return diff.days
    
    def get_host_email_text(self, reservation):
        diff = self.how_late(reservation)
        due = 0
        if diff <= 10:
            ekh = 11 - diff
            due += reservation.total_price * ekh * 0.1
        text = 'رزرو با کد '
        text += reservation.id
        text += ' لغو شده است. '

        if due > 0:
            text += ' مقدار '
            text += str(due)
            text += ' به حساب شما واریز خواهد شد.'
        
        return text

    def get_guest_email_text(self, reservation):
        host = reservation.roominfo.all()[0].room.accommodation.owner
        diff = self.how_late(reservation)
        due = 0
        if diff <= 10:
            ekh = 11 - diff
            due += reservation.total_price *(1 - ekh * 0.1)
        text = 'رزرو با کد '
        text += reservation.id
        text += ' لغو شده است. '

        if due > 0:
            text += ' مقدار '
            text += str(due)
            text += ' به حساب شما واریز خواهد شد.'
        
        return text
    
    def post(self, request, *args, **kwargs):
        res_id = kwargs['resid']
        reservation = get_object_or_404(Reservation, res_id)
        reservation.is_canceled = True
        reservation.save()
        host_email, guest_email = reservation.roominfo.all()[0].room.accommodation.owner.email, reservation.reserver.email
        send_mail(
            'لغو رزرو',
            self.get_host_email_text,
            DEFAULT_FROM_EMAIL,
            [host_email],
            fail_silently=False,
        )
        send_mail(
            'لغو رزرو',
            self.get_guest_email_text,
            DEFAULT_FROM_EMAIL,
            [guest_email],
            fail_silently=False,
        )
        messages.success(request, 'لغو رزرو با موفقیت انجام شد.')
        url = '/accommodation/' + str(reservation.roominfo.all()[0].room.accommodation.pk)
        return redirect(url)


class PaymentView(View):
    template_name = 'bank.html'

    def get(self, request, *args, **kwargs):
        res_id = kwargs['resid']
        amount = get_object_or_404(Reservation, id=res_id)
        amount = amount.total_price
        return render(request, self.template_name, {'amount': amount, 'reservation_id': res_id})

    def post(self, request, *args, **kwargs):
        reservation_id = kwargs['resid']
        form = PaymentForm(request.POST)
        success = ''
        if form.is_valid():
            success = form.cleaned_data.get('success')
            if success == 'success':
                success = True
            else:
                success = False
            reservation = get_object_or_404(Reservation, pk=reservation_id)
            Transaction.objects.create(is_successful=success, reservation=reservation)
            acc_id = reservation.roominfo.all()[0].room.accommodation.pk
            if success:
                messages.success(request, 'پرداخت شما با موفقیت انجام شد.')
            else:
                messages.error(request, 'پرداخت شما با موفقیت انجام نشد. دوباره تلاش کنید.')
            url = '/accommodation/' + str(acc_id)
            return redirect(url)
