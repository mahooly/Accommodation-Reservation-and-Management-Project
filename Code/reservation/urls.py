from reservation import views
from django.urls import path

urlpatterns = [
    path('reservation/<int:rid>/', views.MakeReservation.as_view(), name='make_reservation'),
    path('payment/<int:resid>/', views.PaymentView.as_view(), name='payment'),
    path('cancel_reservation/<int:resid>/', views.CancelReservation.as_view(), name='cancel_reservation'),
    path('accommodation_reservations/<int:pk>', views.AccommodationReservationList.as_view(),
         name='accommodation_reserve'),
    path('user_dashborad/reservations', views.UserReservationList.as_view(),
         name='user_reserve'),
]
