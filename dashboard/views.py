from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from database.models import PaceUser, Mission

@login_required
def dashboard(request):
    """Render dashboard only if user is logged in as either Student or Teacher

    For now, dashboard only shows user name and user type.
    TODO: dashboard will list classes that the user is associated with.
    """
    # get user type
    user = request.user
    if user.is_student:
        user_type = "Student"
    elif user.is_teacher:
        user_type = "Teacher"
    else:
        user_type = "Admin"

    all_mission = Mission.objects.filter(schoolclass__paceuser=user)

    context = {
        'user_type': user_type,
        'user': user,
        'classes': user.schoolclasses.all(),
        'all_mission': all_mission,
    }

    return render(request, 'dashboard.html', context=context)
