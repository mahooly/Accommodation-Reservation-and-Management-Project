from django import forms


class MakeReservationForm(forms.Form):
    check_in = forms.CharField(max_length=20)
    check_out = forms.CharField(max_length=20)
    how_many = forms.CharField(max_length=1)


class PaymentForm(forms.Form):
    success = forms.CharField(max_length=10)
