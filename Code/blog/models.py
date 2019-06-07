from django.db import models
from registration.models import CustomUser
from accommodation.models import Accommodation


class Post(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="../media/blog_pics/", default="../media/blog_pics/no-picture.png")
    province = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-date']


class Comment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
