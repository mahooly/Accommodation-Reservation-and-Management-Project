from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MakeReservationForm
from .models import Reservation, Transaction
from accommodation.models import Room, RoomInfo


class ReservationDetail(View):
    template_name = "reservation/reservation-detail.html"

    def get(self, request):
        return render(request, self.template_name)


class AllReservations(View):
    template_name = "reservation/all-reservations.html"

    def get(self, request):
        return render(request, self.template_name)


class MakeReservation(View):

    def convert_string_to_date(self, date_string):
        return datetime.datetime.strptime(date_string, self.format)

    def get_available_room_infos(self, room, form):
        check_in, check_out = form.cleaned_data['check_in'], form.cleaned_data['check_out']
        availableRoomInfos = RoomInfo.objects.all().exclude(
                    Q(reservation__check_in__range=(check_in, check_out - timedelta(days=1))) |
                    Q(reservation__check_out__range=(check_in + timedelta(days=1), check_out))).filter(
                    out_of_service=False, room=room)
        return availableRoomInfos

    def post(self, request, *args, **kwargs):
        form = MakeReservationForm(request.POST)
        room_id = kwargs['rid']
        room = get_object_or_404(Room, pk=room_id)
        if form.is_valid():
            how_many = form.cleaned_data.get('how_many')
            available_room_infos = self.get_available_room_infos(room, form)
            count = 0
            reserve = Reservation.create(reserver=request.user, check_in=form.cleaned_data['check_in'], check_out=form.cleaned_data['check_out'])
            reserve.save()
            for room_info in available_room_infos:
                if count < how_many:
                    reserve.room_info.add(room_info)
                    count += 1
            messages.success(request, 'رزرو شما با موفقیت ثبت شد.')
            url = '/payment/' + str(reservation_id)
            return redirect(url)
        else:
            messages.error(request, 'در رزرو کردن اتاق مشکلی پیش آمده است. لطفاً دوباره تلاش کنید.')
            accommodation_id = room.accommodation.pk
            url = '/accommodation/' + str(accommodation_id)
            return redirect(url)

class CancelReservation(View):
    def post(self, request, *args, **kwargs):
        res_id = kwargs['resid']
        reservation = get_object_or_404(Reservation, res_id)
        reservation.is_canceled = True
        reservation.save()
        messages.success(request, 'لغو رزرو با موفقیت انجام شد.')
        url = '/accommodation/' + str(reservation.room_info__set[0].room.accommodation.pk)
        return redirect(url)

class PaymentView(View):
    template_name = 'bank.html'
    def get(self, request, *args, **kwargs):
        res_id = kwargs['resid']
        amount = get_object_or_404(Reservation, res_id).total_price
        return render(request, self.template_name, {'amount': amount, 'reservation_id': res_id})


class PaymentSuccessView(View): 

    def get(self, request, *args, **kwargs):
        reservation_id = kwargs['resid']
        success = kwargs['success']
        if success == 'success': success = True
        else: success = False
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        transaction = Transaction.objects.create(is_success=success)
        transaction.reservation = reservation
        transaction.save()
        acc_id = reservation.roominfo__set[0].room.accommodation.pk
        if success == True : messages.success(request, 'پرداخت شما با موفقیت انجام شد.')
        else: messages.error(request, 'پرداخت شما با موفقیت انجام نشد. دوباره تلاش کنید.')
        # messages.success(request, 'پرداخت شما با موفقیت انجام شد.')
        url = '/accommodation/' + str(acc_id)
        return redirect(url)