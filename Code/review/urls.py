from django.urls import path

from review import views

urlpatterns = [
    path('accommodation/<int:accid>/review', views.CreateReview.as_view(), name='create_review'),
]
