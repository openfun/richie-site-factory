"""Pipeline used only for the demo to add all permissions to a staff user."""


def set_super_user(strategy, details, backend, user=None, *args, **kwargs):
    """
    set user.is_superuser to True if there is_staff is set in the details and the user exists.
    """
    if details.get("is_staff", False) and user:
        user.is_superuser = True
        strategy.storage.user.changed(user)
