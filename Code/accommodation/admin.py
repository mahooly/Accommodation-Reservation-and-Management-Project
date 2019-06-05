from django.contrib import admin
from .models import Accommodation, Room, Image

# Register your models here.
admin.site.register(Accommodation)
admin.site.register(Room)
admin.site.register(Image)