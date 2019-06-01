from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from search_index import views

urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
]