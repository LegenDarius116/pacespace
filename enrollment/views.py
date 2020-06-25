from django.db import models
from django.shortcuts import render, redirect
from database.models import SchoolClass, PaceUser
from database.user_functions import *

def enrollment(request):
    if request.user.is_authenticated:
        user = request.user
        # if request.method == "POST":
        return render(request, "enrollment.html", context=context)
    else:
        return redirect('index')