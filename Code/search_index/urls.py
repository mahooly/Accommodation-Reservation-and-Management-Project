from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from search_index import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('search_location/', views.LocationSearchView.as_view(), name='search_location'),
]
