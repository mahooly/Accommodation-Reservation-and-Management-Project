from django.conf.urls import url
from django.urls import path
from accommodation import views

urlpatterns = [
    path('create_accommodation/', views.CreateAccommodationView.as_view(), name='create_accommodation'),
    path('accommodation/<int:pk>/', views.AccommodationDetailView.as_view(), name='accommodation_detail'),
    path('room/<int:accid>/', views.CreateRoomView.as_view(), name='create_room'),
    path('delete_accommodation/<int:pk>/', views.DeleteAccommodation.as_view(), name='delete_accommodation'),
    path('edit_accommodation/<int:pk>/', views.EditAccommodation.as_view(), name='edit_accommodation'),
    path('accommodation_rooms/<int:pk>/', views.AccommodationRoomsView.as_view(), name='accommodation_rooms'),
    path('image/<int:pk>/', views.DeleteImage.as_view(), name='delete_image'),
]
