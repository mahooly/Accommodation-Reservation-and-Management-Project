from django.shortcuts import render
from django.views import View
from .forms import PaymentForm
from .models import Transaction
from django.utils.decorators import method_decorator
from registration.decorators import user_is_confirmed
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

@method_decorator([login_required, user_is_confirmed], name='dispatch')
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
            acc_id = reservation.roominfo.first().room.accommodation.pk
            if success:
                messages.success(request, 'پرداخت شما با موفقیت انجام شد.')
                return redirect('user_reserve')
            else:
                messages.error(request, 'پرداخت شما با موفقیت انجام نشد. دوباره تلاش کنید.')
                url = '/accommodation/' + str(acc_id)
                return redirect(url)
