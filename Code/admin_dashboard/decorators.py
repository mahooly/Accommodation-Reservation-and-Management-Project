from django.shortcuts import redirect


def user_is_superuser(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
