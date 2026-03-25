from django.shortcuts import redirect

# Authontication and authorization middlewares for buyer app

def auth(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('buyer-login')
        return view_func(request, *args, **kwargs)
    return wrapped_view


def loggedin_auth(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('buyer-dashboard')
        return view_func(request, *args, **kwargs)
    return wrapped_view