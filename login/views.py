from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login

# Create your views here.

def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(data=request.POST)
        print(login_form)
        try:
            login_form.confirm_login_allowed(request.user)
        except:
            import traceback
            traceback.print_exc()
            return render(request, "login/login.html", {"login_form": login_form})
        return redirect('index')

    else:
        login_form = LoginForm()
    return render(request, "login/login.html", {"login_form": login_form})
