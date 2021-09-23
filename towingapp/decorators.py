from django.http import HttpResponse, request
from django.shortcuts import redirect

def unauthenticated_user(view_funct):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        else:
            return view_funct(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_funct):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_funct(request, *args, **kwargs)
            else:
                return HttpResponse('you are not allowed to view this page')
        return wrapper_func
    return decorator


def admin_only(view_funct):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('profile')

        elif group == 'admin':
            return view_funct(request, *args, **kwargs)
        else:
            return redirect('payment')
    
    return wrapper_func