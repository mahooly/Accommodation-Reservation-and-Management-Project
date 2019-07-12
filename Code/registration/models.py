from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from datetime import datetime


class CustomUser(AbstractUser):
    gender = models.CharField(max_length=10, default='مرد')
    birth_date = models.DateField(null=True)
    image = models.ImageField(upload_to='../media/profile_pics/', default='../media/profile_pics/no-picture.png')
    is_host = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def age(self):
        today = datetime.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    @property
    def _full_name(self):
        return self.first_name + ' ' + self.last_name


class Host(models.Model):
    user = models.OneToOneField(CustomUser, related_name='host', on_delete=models.CASCADE)
    passport_pic = models.ImageField(upload_to='../media/passport_pics/',
                                     default='../media/profile_pics/no-picture.png')
    home_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=40)
