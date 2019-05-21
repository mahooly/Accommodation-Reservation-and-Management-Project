from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import GENDER_CHOICES
import datetime


class CustomUser(AbstractUser):
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    birth_date = models.DateField(default=datetime.datetime.now())
    image = models.ImageField(upload_to='../media/profile_pics/', default='../media/profile_pics/no-picture.png')
    is_host = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Host(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    passport_pic = models.ImageField(upload_to='../media/passport_pics/', default='../media/profile_pics/no-picture.png')
    home_address = models.TextField()
    phone_number = models.TextField()