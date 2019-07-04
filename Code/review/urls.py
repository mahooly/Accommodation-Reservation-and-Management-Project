from django.urls import path

from review import views

urlpatterns = [
    path('accommodation/<int:accid>/review', views.CreateReview.as_view(), name='create_review'),
    path('accommodation_reviews/<int:pk>', views.AccommodationReviews.as_view(), name='accommodation_review'),
    path('reply/<int:pk>', views.CreateReply.as_view(), name='create_reply'),
]
