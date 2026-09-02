from functools import wraps
from django.shortcuts import redirect


def login_required(view_function):
    """
    Require a valid authenticated session before accessing a view.
    """

    @wraps(view_function)
    def wrapper(request, *args, **kwargs):

        if not request.session.get("user_id"):
            return redirect("login")

        return view_function(request, *args, **kwargs)

    return wrapper