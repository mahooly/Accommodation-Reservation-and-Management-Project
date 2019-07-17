from django.urls import path

from admin_dashboard import views

urlpatterns = [
    path('admin_dashboard/', views.AdminDashboard.as_view(), name='admin_dashboard'),
    path('admin_dashboard/users', views.AdminUserDashboard.as_view(), name='admin_dashboard_users'),
    path('admin_dashboard/accommodations', views.AdminAccommodationDashboard.as_view(),
         name='admin_dashboard_accommodations'),
    path('delete_user/<int:pk>/', views.DeleteUser.as_view(), name='delete_user'),
    path('authenticate_accommodation/<int:pk>/', views.AuthenticateAccommodation.as_view(),
         name='authenticate_accommodation'),
]
