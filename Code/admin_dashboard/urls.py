from .decorators import user_is_superuser
from django.urls import path
from django.views.generic import TemplateView

from admin_dashboard import views

urlpatterns = [
    path('admin_dashboard/', user_is_superuser(TemplateView.as_view(template_name="admin_dashboard/admin_dashboard.html")),
         name='admin_dashboard'),
    path('admin_dashboard/users', views.AdminUserDashboard.as_view(), name='admin_dashboard_users'),
    path('admin_dashboard/accommodations', views.AdminAccommodationDashboard.as_view(),
         name='admin_dashboard_accommodations'),
    path('delete_user/<int:pk>/', views.DeleteUser.as_view(), name='delete_user'),
    path('authenticate_accommodation/<int:pk>/', views.AuthenticateAccommodation.as_view(),
         name='authenticate_accommodation'),
]
