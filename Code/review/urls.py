from django.urls import path

from review import views

urlpatterns = [
    path('accommodation/<int:accid>/comment', views.CreateComment.as_view(), name='create_comment'),
]
