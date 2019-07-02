from django.db import models

from .choices import BED_TYPE_CHOICES, ACCOMMODATION_TYPE_CHOICES
from registration.models import Host, CustomUser


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


class Room(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    amenity = models.ManyToManyField(Amenity)
    description = models.TextField()
    bed_type = models.CharField(max_length=20, choices=BED_TYPE_CHOICES)
    number_of_guests = models.IntegerField()
    image = models.ImageField(upload_to='../media/room_pics/')

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
