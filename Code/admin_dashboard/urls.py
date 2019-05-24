from django.conf.urls import url
from django.urls import path
from admin_dashboard import views

urlpatterns = [
    path('admin_dashboard/', views.AdminDashboard.as_view(), name='admin_dashboard'),
    path('delete_user/<int:pk>/', views.DeleteUser.as_view(), name='delete_user'),
    path('delete_accommodation/<int:pk>/', views.DeleteAccommodation.as_view(), name='delete_accommodation'),
]