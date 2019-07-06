from django.db import models
from registration.models import CustomUser
from accommodation.models import RoomInfo, Amenity, Room


class Reservation(models.Model):
    reserver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    roominfo = models.ManyToManyField(RoomInfo)
    check_in = models.DateField()
    check_out = models.DateField()
    is_canceled = models.BooleanField(default=False)

    @property
    def is_confirmed(self):
        try:
            return Transaction.objects.filter(reservation=self.pk).is_successful
        except:
            return False

    @property
    def total_price(self):
        return self.roominfo.all()[0].room.price * self.roominfo.count()


class Transaction(models.Model):
    is_successful = models.BooleanField(default=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.reservation.roominfo.all()[0].room.price * self.reservation.roominfo.count()
