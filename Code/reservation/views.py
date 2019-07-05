from django.shortcuts import render
from django.views import View

# Create your views here.

class ReservationDetail(View):
    template_name = "reservation/reservation-detail.html"

    def get(self, request):
        return render(request, self.template_name)



class AllReservations(View):
    template_name = "reservation/all-reservations.html"

    def get(self, request):
        return render(request, self.template_name)