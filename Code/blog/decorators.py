from django.shortcuts import get_object_or_404, redirect
from functools import wraps

from blog.models import Comment
from registration.models import CustomUser


def user_same_as_comment_user_or_admin(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        comment = get_object_or_404(Comment, id=kwargs['id'])
        if user == comment.user or user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')

    return wrap


def user_same_as_dashboard_user(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        dash_user = get_object_or_404(CustomUser, id=kwargs['uid'])
        if user == dash_user:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')

    return wrap
