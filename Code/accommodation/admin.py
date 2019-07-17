from django.contrib import admin
from .models import Accommodation, Room, Image, Amenity, RoomInfo, TouristAttraction, RoomOutOfService

admin.site.register(Accommodation)
admin.site.register(Room)
admin.site.register(RoomInfo)
admin.site.register(Image)
admin.site.register(Amenity)
admin.site.register(TouristAttraction)
admin.site.register(RoomOutOfService)
