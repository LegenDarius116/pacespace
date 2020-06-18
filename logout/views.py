from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_user(request):
    """If user is logged in, logs them out. Then redirects to landing page."""
    if request.user.is_authenticated:
        print(f"Logging out user {request.user.username}")
        logout(request)
    else:
        print("No authenticated users found")

    return redirect('/')
