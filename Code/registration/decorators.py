from django.shortcuts import redirect
from functools import wraps


def user_is_host(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_host:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')

    return wrap


def user_is_confirmed(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_confirmed:
            return function(request, *args, **kwargs)
        else:
            return redirect('activation_required')

    return wrap
