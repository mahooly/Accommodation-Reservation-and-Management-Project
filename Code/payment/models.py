from django.db import models
from reservation.models import Reservation


class Transaction(models.Model):
    is_successful = models.BooleanField(default=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    coefficient = models.IntegerField(default=1)

    @property
    def total_price(self):
        stay_len = self.reservation.check_out - self.reservation.check_in
        stay_len = stay_len.days
        return self.coefficient * self.reservation.roominfo.first().room.price * stay_len * self.reservation.roominfo.count()
