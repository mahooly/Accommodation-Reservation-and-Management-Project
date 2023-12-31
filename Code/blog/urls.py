from django.contrib.auth.decorators import login_required
from django.urls import path
from blog import views
from .decorators import user_same_as_dashboard_user
from registration.decorators import user_is_confirmed

urlpatterns = [
    path('user/<int:uid>/blog', views.BlogListView.as_view(), name='blog_list'),
    path('blog', views.BlogListView.as_view(), name='blog'),
    path('user_dashboard/<int:uid>',
         login_required(user_is_confirmed(
             user_same_as_dashboard_user(
                 views.BlogListView.as_view(template_name='registration/user_dashboard.html')))),
         name='user_dashboard'),
    path('user/<int:uid>/blog/create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blog/post/<int:pk>/', views.BlogDetailView.as_view(),
         name='blog_detail'),
    path('post/<int:pk>/comment/', views.CreateCommentView.as_view(),
         name='post_comment'),
    path('delete_comment/<int:id>/',
         views.CommentDelete.as_view(), name='comment_delete'),
    path('user/<int:uid>/blog/<int:blog_id>/edit/', views.BlogEditView.as_view(), name='blog_edit')
]
