
from django.urls import path
from feedback import views

urlpatterns = [
    path('feedback/<int:person_id>',views.FeedBackListView.as_view(), name='feedback_list'),
]