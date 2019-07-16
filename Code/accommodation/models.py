from django.db import models
from django.db.models import Min, Max, deletion

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
    latitude = models.DecimalField(max_digits=16, decimal_places=14, null=True, blank=True)
    longitude = models.DecimalField(max_digits=16, decimal_places=14, null=True, blank=True)
    amenity = models.ManyToManyField(Amenity)
    is_authenticated = models.BooleanField(default=False)

    @property
    def single_beds(self):
        try:
            return Room.objects.get(accommodation=self, bed_type='Single').how_many
        except Room.DoesNotExist:
            return 0

    @property
    def double_beds(self):
        try:
            return Room.objects.get(accommodation=self, bed_type='Double').how_many
        except Room.DoesNotExist:
            return 0

    @property
    def twin_beds(self):
        try:
            return Room.objects.get(accommodation=self, bed_type='Twin').how_many
        except Room.DoesNotExist:
            return 0

    @property
    def guests(self):
        rooms = Room.objects.filter(accommodation=self)
        guests = 0
        for r in rooms:
            guests += (r.how_many * r.number_of_guests)
        return guests

    @property
    def rooms(self):
        return self.single_beds + self.double_beds + self.twin_beds

    @property
    def overall_score(self):
        score_sum = 0
        num = self.review_set.count()
        if num == 0:
            return 0.0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.overall
        return round(score_sum / num, 1)

    @property
    def overall_cleanliness(self):
        score_sum = 0
        num = self.review_set.count()
        if num == 0:
            return 0.0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_cleanliness
        return round(score_sum / num, 1)

    @property
    def overall_comfort(self):
        score_sum = 0
        num = self.review_set.count()
        if num == 0:
            return 0.0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_comfort
        return round(score_sum / num, 1)

    @property
    def overall_location(self):
        score_sum = 0
        num = self.review_set.count()
        if num == 0:
            return 0.0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_location
        return round(score_sum / num, 1)

    @property
    def overall_facilities(self):
        score_sum = 0
        num = self.review_set.count()
        if num == 0:
            return 0.0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_facilities
        return round(score_sum / num, 1)

    @property
    def overall_staff(self):
        score_sum = 0
        num = self.review_set.count()
        if num == 0:
            return 0.0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_staff
        return round(score_sum / num, 1)

    @property
    def overall_value(self):
        score_sum = 0
        num = self.review_set.count()
        if num == 0:
            return 0.0
        for r in self.review_set.all():
            if r.rating:
                score_sum += r.rating.score_value
        return round(score_sum / num, 1)

    @property
    def min_price(self):
        return self.room_set.all().aggregate(Min('price')).get('price__min')

    @property
    def max_price(self):
        return self.room_set.all().aggregate(Max('price')).get('price__max')

    def __str__(self):
        return self.title


class Room(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    amenity = models.ManyToManyField(Amenity)
    description = models.TextField()
    bed_type = models.CharField(max_length=20, choices=BED_TYPE_CHOICES)
    number_of_guests = models.IntegerField()
    image = models.ImageField(upload_to='../media/room_pics/')
    price = models.IntegerField(default=0)

    @property
    def how_many(self):
        return RoomInfo.objects.filter(room=self).count()

    def __str__(self):
        return self.accommodation.title


class Image(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='../media/house_pics/')


class RoomInfo(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number = models.IntegerField(default=None, null=True)

    def __str__(self):
        return str(self.room) + self.room.bed_type


class RoomOutOfService(models.Model):
    room_info = models.ForeignKey(RoomInfo, on_delete=deletion.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
