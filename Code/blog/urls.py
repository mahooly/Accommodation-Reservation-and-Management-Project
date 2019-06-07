from django.urls import path
from blog import views
from blog.models import Post

urlpatterns = [
    path('user/<int:uid>/blog', views.BlogListView.as_view(), name='blog_list'),
    path('blog', views.BlogListView.as_view(queryset=Post.objects.all()), name='blog'),
    path('user_dashboard/<int:uid>/blog', views.BlogListView.as_view(template_name='registration/user_dashboard.html'),
         name='user_dashboard'),
    path('host_dashboard/<int:uid>/blog', views.BlogListView.as_view(template_name='blog/host_blog.html'),
         name='host_blog'),
    path('user/<int:uid>/blog/create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blog/post/<int:pk>', views.BlogDetailView.as_view(),
         name='blog_detail'),
    path('post/<int:pk>/comment', views.CreateCommentView.as_view(),
         name='post_comment'),
    path('delete_comment/comment_id=<int:comment_id>/username=<str:username>/feed_id=<int:feed_id>',
         views.CommentDelete.as_view(), name="comment_delete")
]
