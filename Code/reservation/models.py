from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncMonth

from registration.models import CustomUser
from accommodation.models import RoomInfo, Amenity, Room


class ReservationManager(models.Manager):
    def get_count_by_month(self):
        return self.annotate(month=TruncMonth('transaction__creation_date')).values(
            'month').annotate(count=Count('id'))

    def get_cancelled_count_by_month(self):
        return self.filter(is_canceled=True).annotate(
            month=TruncMonth('transaction__creation_date')).values(
            'month').annotate(count=Count('id'))


class Reservation(models.Model):
    reserver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    roominfo = models.ManyToManyField(RoomInfo)
    check_in = models.DateField()
    check_out = models.DateField()
    is_canceled = models.BooleanField(default=False)

    objects = ReservationManager()

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
