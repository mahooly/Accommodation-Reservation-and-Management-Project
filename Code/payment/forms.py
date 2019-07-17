from django import forms

class PaymentForm(forms.Form):
    success = forms.CharField(max_length=10)