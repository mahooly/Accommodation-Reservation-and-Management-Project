from django.shortcuts import redirect, get_object_or_404
from functools import wraps

from accommodation.models import Accommodation, Image


def user_same_as_accommodation_user(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if 'accid' in kwargs.keys():
            acc = get_object_or_404(Accommodation, id=kwargs['accid'])
        else:
            acc = get_object_or_404(Accommodation, id=kwargs['pk'])
        if user == acc.owner.user:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrap


def user_same_as_image_user(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        image = get_object_or_404(Image, id=kwargs['pk'])
        image_user = image.accommodation.owner.user
        if user == image_user:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrap


def user_host_or_superuser(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_host or user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrap
