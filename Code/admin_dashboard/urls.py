from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from admin_dashboard import views

urlpatterns = [
    path('admin_dashboard/', TemplateView.as_view(template_name="admin_dashboard.html"), name='admin_dashboard'),
    path('admin_dashboard/users', views.AdminUserDashboard.as_view(), name='admin_dashboard_users'),
    path('delete_user/<int:pk>/', views.DeleteUser.as_view(), name='delete_user'),
    path('delete_accommodation/<int:pk>/', views.DeleteAccommodation.as_view(), name='delete_accommodation'),
    path('authenticate_accommodation/<int:pk>/', views.AuthenticateAccommodation.as_view(), name='authenticate_accommodation'),
]
