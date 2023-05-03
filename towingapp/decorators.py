from django.http import HttpResponse, request
from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.sessions.models import Session


def prevent_multiple_users(func):
    def wrapper(request, *args, **kwargs):
        # Get the session key of the current user
        session_key = request.session.session_key

        # Get the User model
        User = get_user_model()

        # Find all sessions with the same session key
        sessions = Session.objects.filter(session_key=session_key)

        # Find all users associated with those sessions
        users = User.objects.filter(id__in=[s.get_decoded().get('_auth_user_id') for s in sessions])

        # If there is more than one user, redirect to an error page
        if len(users) > 1:
            return redirect('profile')

        # Otherwise, call the original view function
        return func(request, *args, **kwargs)

    return wrapper



def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile', MyUser_str=request.user.username)
        else:
            return view_func(request, *args, **kwargs)
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