from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import GENDER_CHOICES
import datetime


class CustomUser(AbstractUser):
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    birth_date = models.DateField()
    image = models.ImageField(upload_to='../media/profile_pics/', default='../media/profile_pics/no-picture.png')
    is_host = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def _get_age(self):
        today = datetime.date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    age = property(_get_age)


class Host(models.Model):
    user = models.OneToOneField(CustomUser, related_name='host', on_delete=models.CASCADE)
    passport_pic = models.ImageField(upload_to='../media/passport_pics/',
                                     default='../media/profile_pics/no-picture.png')
    home_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=40)
