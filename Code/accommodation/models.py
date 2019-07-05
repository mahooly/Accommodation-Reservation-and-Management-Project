from django.db import models

from .choices import BED_TYPE_CHOICES, ACCOMMODATION_TYPE_CHOICES
from registration.models import Host, CustomUser
from django.db.models import Q


class Amenity(models.Model):
    name = models.CharField(max_length=20)
    label = models.CharField(max_length=6)

    def __str__(self):
        return self.name


class Accommodation(models.Model):
    owner = models.ForeignKey(Host, related_name='owner', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField()
    accommodation_type = models.CharField(max_length=20, choices=ACCOMMODATION_TYPE_CHOICES)
    province = models.CharField(max_length=30, default='تهران')
    city = models.CharField(max_length=30, default='تهران')
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    amenity = models.ManyToManyField(Amenity)

    is_authenticated = models.BooleanField(default=False)

    def _get_singles(self):
        try:
            return Room.objects.get(accommodation=self, bed_type='Single').how_many
        except Room.DoesNotExist:
            return 0

    single_beds = property(_get_singles)

    def _get_doubles(self):
        try:
            return Room.objects.get(accommodation=self, bed_type='Double').how_many
        except Room.DoesNotExist:
            return 0

    double_beds = property(_get_doubles)

    def _get_twins(self):
        try:
            return Room.objects.get(accommodation=self, bed_type='Twin').how_many
        except Room.DoesNotExist:
            return 0

    twin_beds = property(_get_twins)

    def _get_guests(self):
        rooms = Room.objects.filter(accommodation=self)
        guests = 0
        for r in rooms:
            guests += (r.how_many * r.number_of_guests)
        return guests

    guests = property(_get_guests)

    def _get_all_rooms(self):
        return self.single_beds + self.double_beds + self.twin_beds

    rooms = property(_get_all_rooms)

    @property
    def overall_score(self):
        score_sum = 0
        num = 0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.overall
                num += 1
        return round(score_sum / num, 1)

    @property
    def overall_cleanliness(self):
        score_sum = 0
        num = 0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_cleanliness
                num += 1
        return round(score_sum / num, 1)

    @property
    def overall_comfort(self):
        score_sum = 0
        num = 0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_comfort
                num += 1
        return round(score_sum / num, 1)

    @property
    def overall_location(self):
        score_sum = 0
        num = 0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_location
                num += 1
        return round(score_sum / num, 1)

    @property
    def overall_facilities(self):
        score_sum = 0
        num = 0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_facilities
                num += 1
        return round(score_sum / num, 1)

    @property
    def overall_staff(self):
        score_sum = 0
        num = 0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_staff
                num += 1
        return round(score_sum / num, 1)

    @property
    def overall_value(self):
        score_sum = 0
        num = 0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_value
                num += 1
        return round(score_sum / num, 1)


class Room(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    amenity = models.ManyToManyField(Amenity)
    description = models.TextField()
    bed_type = models.CharField(max_length=20, choices=BED_TYPE_CHOICES)
    number_of_guests = models.IntegerField()
    image = models.ImageField(upload_to='../media/room_pics/')
    price = models.IntegerField(default=0)

    #def is_available(self, check_in, check_out):
        #badReservations = Reservation.filter(Q(check_in__range(check_in, check_out)) | Q(check_in__range(check_in, check_out)))
        #roomInfos = RoomInfo.exclude(room=self)
        #for roomInf

    @property
    def how_many(self):
        return RoomInfo.objects.filter(room=self).count()

    @property
    def reservable_count(self):
        return RoomInfo.objects.filter(room=self, is_reserved=False).count()


class Image(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='../media/house_pics/')


class RoomInfo(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_reserved = models.BooleanField(default=False)
    out_of_service = models.BooleanField(default=False)
