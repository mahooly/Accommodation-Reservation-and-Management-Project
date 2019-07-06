from reservation import views
from django.urls import path

urlpatterns = [
    path('reservation-detail', views.ReservationDetail.as_view(), name="reservation_detail"),
    path('reservation-all', views.AllReservations.as_view(), name="reservation_all"),
    path('reservation/<int:rid>/', views.MakeReservation.as_view(), name='make_reservation'),
    path('payment/<int:resid>/', views.PaymentView.as_view(), name='payment'),
    path('payment_success/<int:resid>/<str:success>', views.PaymentSuccessView.as_view(), name='payment_result'),
    path('cancel_reservation/<int:resid>/', views.CancelReservation.as_view(), name='cancel_reservation'),
]
