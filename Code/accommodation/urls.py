from django.urls import path

from accommodation import views

urlpatterns = [
    path('create_accommodation/', views.CreateAccommodationView.as_view(), name='create_accommodation'),
    path('create_amenity/', views.CreateAmenityView.as_view(), name='create_amenity'),
    path('accommodation/<int:pk>/', views.AccommodationDetailView.as_view(), name='accommodation_detail'),
    path('room/<int:accid>/', views.CreateRoomView.as_view(), name='create_room'),
    path('accommodation/<int:pk>/delete', views.DeleteAccommodation.as_view(), name='delete_accommodation'),
    path('accommodation/<int:pk>/edit/', views.EditAccommodation.as_view(), name='edit_accommodation'),
    path('image/<int:pk>/', views.DeleteImage.as_view(), name='delete_image'),
    path('accommodation/<int:pk>/rooms', views.RoomListView.as_view(), name='room_list'),
    path('accommodation/<int:pk>/rooms/stats', views.RoomInfoStatsView.as_view(), name='room_stats'),
    path('delete_room/<int:pk>/', views.DeleteRoomView.as_view(), name='delete_room'),
    path('create_room/<int:pk>/', views.CreateRoomInfo.as_view(), name='create_room_info'),
    path('change_room/<int:pk>/', views.ChangeRoomInfoView.as_view(), name='change_room_info'),
    path('delete_room_info/<int:pk>/', views.DeleteRoomInfoView.as_view(), name='delete_room_info'),
]
