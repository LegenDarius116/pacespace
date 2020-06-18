from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login

# Create your views here.

def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(data=request.POST)
        print(login_form)
        try:
            if login_form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                # Redirect to a success page.
                if request.user.is_authenticated is True:
                    return redirect('index')
        except:
            import traceback
            traceback.print_exc()
            return render(request, "login/login.html", {"login_form": login_form})

    else:
        login_form = LoginForm()
    return render(request, "login/login.html", {"login_form": login_form})
