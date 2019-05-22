from django.db import models
from .choices import BED_TYPE_CHOICES,ACCOMMODATION_TYPE_CHOICES
from registration.models import Host

# Create your models here.

class Amenity(models.Model):
    has_wifi = models.BooleanField(default = False)
    has_tv = models.BooleanField(default = False)
    has_washer = models.BooleanField(default = False)
    has_warm_ac = models.BooleanField(default = False)
    has_cool_ac = models.BooleanField(default = False)
    has_parking = models.BooleanField(default = False)
    has_kitchen = models.BooleanField(default = False)
    has_utensils = models.BooleanField(default = False)
    has_fridge = models.BooleanField(default = False)
    has_oven = models.BooleanField(default = False)
    has_bedsheets = models.BooleanField(default = False)
    

class Accommodation(models.Model):
    owner = models.ForeignKey(Host, related_name='owner', on_delete=models.CASCADE)
    
    accommodation_type = models.CharField(max_length = 20, choices = ACCOMMODATION_TYPE_CHOICES)
    city = models.CharField(max_length = 20, default = 'تهران')
    address = models.CharField(max_length = 100)
    amenity = models.OneToOneField(Amenity, related_name = 'accommodation', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='../media/house_pics/', default='../media/house_pics/no-picture.png')


class Room(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    amenity = models.OneToOneField(Amenity, related_name='room', on_delete=models.CASCADE)

    bed_type = models.CharField(max_length = 20, choices = BED_TYPE_CHOICES)
    number_of_guests = models.IntegerField()

    how_many = models.IntegerField(default=1)





