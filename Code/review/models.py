from django.db import models
from django.db.models import deletion

from accommodation.models import Accommodation
from registration.models import CustomUser


class Comment(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=deletion.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='review_user', on_delete=deletion.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
