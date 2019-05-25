from django.conf.urls import url
from django.urls import path
from accommodation import views

urlpatterns = [
    path('create_accommodation/', views.CreateAccommodationView.as_view(), name='create_accommodation'),
    path('accommodation/<int:pk>/', views.AccommodationDetailView.as_view(), name='accommodation_detail'),
    path('room/<int:accid>/', views.CreateRoomView.as_view(), name='create_room'),
]