from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login


def login_view(request):
    login_form = LoginForm(data=request.POST)
    if request.method == "POST":
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

            if request.user.is_authenticated:
                return redirect('/dashboard')

    else:
        login_form = LoginForm()
    return render(request, "login/login.html", {"login_form": login_form})
