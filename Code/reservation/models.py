from django.db import models
from registration.models import CustomUser
from accommodation.models import RoomInfo, Amenity, Room
# Create your models here.


class Reservation(models.Model):
    reserver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    roominfo  = models.ManyToManyField(RoomInfo)
    check_in = models.DateField()
    check_out = models.DateField()
    amenity = models.ManyToManyField(Amenity)

    @property
    def total_price(self):
        return self.roominfo_set[0].room.price * len(self.roominfo_set)




class Transaction(models.Model):
    value = models.IntegerField(default=0)
    is_successful = models.BooleanField(default=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True)