from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse


@login_required
def dashboard(request):
    """Render dashboard only if user is logged in as either Student or Teacher"""
    if not request.user.is_authenticated:
        print("User not authenticated")
        return redirect('/login')

    # render the HTML (keep it simple for now)
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
