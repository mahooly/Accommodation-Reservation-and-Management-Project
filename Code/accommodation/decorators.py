from django.shortcuts import redirect, get_object_or_404

from accommodation.models import Accommodation, Image


def user_same_as_accommodation_user(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if 'accid' in kwargs.keys():
            acc = get_object_or_404(Accommodation, owner__id=kwargs['accid'])
        else:
            acc = get_object_or_404(Accommodation, id=kwargs['pk'])
        if user == acc.owner:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_same_as_image_user(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        image = get_object_or_404(Image, id=kwargs['pk'])
        image_user = image.accommodation.owner
        if user == image_user:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_host_or_superuser(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_host or user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
