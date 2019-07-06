from django.contrib import admin
from .models import Reservation, Transaction

admin.site.register(Reservation)
admin.site.register(Transaction)
