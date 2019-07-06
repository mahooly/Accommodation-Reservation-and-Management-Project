from django import forms

from .models import Reservation

class MakeReservationForm(forms.Form):

    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out', 'how_many']
