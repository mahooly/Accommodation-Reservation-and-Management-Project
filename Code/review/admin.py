from django.contrib import admin

from review.models import Review, Reply, Rating

admin.site.register(Review)
admin.site.register(Reply)
admin.site.register(Rating)
