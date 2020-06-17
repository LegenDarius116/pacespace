from django.shortcuts import render, redirect


def dashboard(request):
    """Render dashboard only if user is logged in as either Student or Teacher"""
    if not request.user.is_authenticated:
        return redirect('/login')

    # render the HTML later
    pass
