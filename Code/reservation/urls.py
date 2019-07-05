from reservation import views
from django.urls import path


urlpatterns = [
    path('reservation-detail', views.ReservationDetail.as_view(), name="reservation_detail"),
    path('reservation-all', views.AllReservations.as_view(), name="reservation_all")
]