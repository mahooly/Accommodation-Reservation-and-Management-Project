from django.db import models
from registration.models import CustomUser
# Create your models here.
from accommodation.models import Accommodation


class Feed(models.Model):
    title = models.CharField(max_length=20 , null=True)
    description = models.TextField(max_length=20 , default='توضیحات')
    #long_description = models.TextField(null=True)
    owner = models.ForeignKey(CustomUser , related_name='feeds', on_delete=models.CASCADE)
    #accommodation = models.ForeignKey(Accommodation, related_name='feeds', on_delete=models.CASCADE)
    province = models.CharField(max_length=30, default='تهران')
    city = models.CharField(max_length=30, default='تهران')
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to="../media/blog_pics/" , default="../media/blog_pics/no-picture.png")
    date = models.DateTimeField(auto_now=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)

    def get_full_name(self):
        return self.owner.get_full_name()
    def get_username(self):
        return self.owner.username


class Comment(models.Model):
    description = models.TextField(default="خالی")
    date = models.DateTimeField(auto_now=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)