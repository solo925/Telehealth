"""
    Decorator that checks if the current user has the specified role.
    
    This decorator can be used to restrict access to a view function based on the
    user's role. If the user does not have the required role, the view function
    will not be executed and an HTTP 403 Forbidden response will be returned.
    
    Args:
        role (str): The required role for the user to access the view function.
    
    Returns:
        A decorator function that can be applied to a view function to enforce the
        role requirement.
    """
def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_role(role):
                return HttpResponseForbidden()
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator