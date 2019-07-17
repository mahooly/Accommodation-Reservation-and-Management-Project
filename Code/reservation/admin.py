from django.contrib import admin
from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_filter = ['check_in', 'check_out']


admin.site.register(Reservation, ReservationAdmin)

