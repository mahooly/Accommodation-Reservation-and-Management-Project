from django.db import models
from registration.models import CustomUser
from accommodation.models import RoomInfo, Amenity, Room


class Reservation(models.Model):
    reserver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    roominfo = models.ManyToManyField(RoomInfo)
    check_in = models.DateField()
    check_out = models.DateField()
    is_canceled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-check_out']

    @property
    def total_price(self):
        stay_len = self.stay_length
        return self.roominfo.first().room.price * stay_len * self.roominfo.count()

    @property
    def stay_length(self):
        stay_len = self.check_out - self.check_in
        return stay_len.days

    @property
    def room_type(self):
        return self.roominfo.first().room.bed_type

    @property
    def accommodation(self):
        return self.roominfo.first().room.accommodation
