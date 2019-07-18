from payment import views

from django.urls import path

urlpatterns = [
    path('payment/<int:resid>/', views.PaymentView.as_view(), name='payment'),
]
