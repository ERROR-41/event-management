# context_processors.py
def user_roles(request):
    """Adds the user's roles to the template context."""
    if request.user.is_authenticated:
        # Get all group names (roles) for the user
        roles = list(request.user.groups.values_list('name', flat=True))
        return {'user_roles': roles}
    return {'user_roles': []}  # Return an empty list if the user is not authenticated