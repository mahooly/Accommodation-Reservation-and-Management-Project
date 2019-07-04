import datetime

from django.db import models
from django.db.models import deletion

from accommodation.models import Accommodation
from registration.models import CustomUser


class Reply(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField()

    @property
    def name_position(self):
        return '{}، {}'.format(self.name, self.position)


class Rating(models.Model):
    score_cleanliness = models.IntegerField()
    score_comfort = models.IntegerField()
    score_location = models.IntegerField()
    score_facilities = models.IntegerField()
    score_staff = models.IntegerField()
    score_value = models.IntegerField()

    @property
    def overall(self):
        score_sum = self.score_cleanliness + self.score_comfort + self.score_facilities + self.score_location + \
                    self.score_staff + self.score_value
        return round(score_sum / 6, 1)


class Review(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=deletion.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='review_user', on_delete=deletion.CASCADE)
    reply = models.OneToOneField(Reply, related_name='review', on_delete=deletion.CASCADE, null=True)
    rating = models.OneToOneField(Rating, related_name='review', on_delete=deletion.CASCADE, null=True)
    title = models.CharField(max_length=50)
    text = models.TextField()
    creation_date = models.DateField(auto_now_add=True)

    @property
    def is_new(self):
        dt = datetime.date.today() - datetime.timedelta(7)
        return self.creation_date >= dt
