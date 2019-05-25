from django.db import models
from django.db.models import Sum

from .choices import BED_TYPE_CHOICES, ACCOMMODATION_TYPE_CHOICES
from registration.models import Host


class Amenity(models.Model):
    has_wifi = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=False)
    has_warm_ac = models.BooleanField(default=False)
    has_cool_ac = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=False)
    has_utensils = models.BooleanField(default=False)
    has_fridge = models.BooleanField(default=False)
    has_oven = models.BooleanField(default=False)
    has_bedsheets = models.BooleanField(default=False)
    has_bathroom = models.BooleanField(default=False)
    has_shower = models.BooleanField(default=False)
    has_tub = models.BooleanField(default=False)
    has_toilet = models.BooleanField(default=False)
    has_hairdryer = models.BooleanField(default=False)
    has_roomservice = models.BooleanField(default=False)
    has_laundry = models.BooleanField(default=False)
    has_elevator = models.BooleanField(default=False)
    has_safe = models.BooleanField(default=False)
    has_iron = models.BooleanField(default=False)


class Accommodation(models.Model):
    owner = models.ForeignKey(Host, related_name='owner', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField()
    accommodation_type = models.CharField(max_length=20, choices=ACCOMMODATION_TYPE_CHOICES)
    city = models.CharField(max_length=20, default='تهران')
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    amenity = models.OneToOneField(Amenity, related_name='accommodation', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='../media/house_pics/', default='../media/house_pics/no-picture.png')

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
    amenity = models.OneToOneField(Amenity, related_name='room', on_delete=models.CASCADE)

    bed_type = models.CharField(max_length=20, choices=BED_TYPE_CHOICES)
    number_of_guests = models.IntegerField()

    how_many = models.IntegerField(default=1)
