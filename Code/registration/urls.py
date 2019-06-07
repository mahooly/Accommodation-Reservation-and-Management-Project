from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from registration import views

urlpatterns = [
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('change_profile/', views.EditProfile.as_view(), name='update_profile'),
    path('become_host/', views.HostRegistration.as_view(), name='become_host'),
    path('user_dashboard/accommodations/', views.HostDashboard.as_view(), name='host_dashboard'),
    path('user/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('user_dashboard/profile/', TemplateView.as_view(template_name='registration/user_profile.html'),
         name='user_profile'),
]
