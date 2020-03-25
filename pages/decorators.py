from django.core.exceptions import PermissionDenied


def user_is_doctor(function):
    def wrap(request,*args,**kwargs):
        if request.user.user_type == 2:
            return function(request,*args,**kwargs)
        else:
            raise PermissionDenied
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_patient(function):
    def wrap(request,*args,**kwargs):
        if request.user.user_type == 1:
            return function(request,*args,**kwargs)
        else:
            raise PermissionDenied
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
