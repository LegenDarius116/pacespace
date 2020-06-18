from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse


@login_required
def dashboard(request):
    """Render dashboard only if user is logged in as either Student or Teacher

    For now, dashboard only shows user name and user type.
    TODO: dashboard will list classes that the user is associated with.
    """
    if request.user.is_student:
        user_type = "Student"
    elif request.user.is_teacher:
        user_type = "Teacher"
    else:
        user_type = "Admin"

    context = {
        'user_name': request.user.username,
        'user_type': user_type,
    }

    return render(request, 'dashboard/index.html', context=context)
