from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, LoginForm


def signup_user(request):
    """Creates user"""
    print('running signup page')
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                usertype = signup_form.cleaned_data["usertype"]
                if usertype == 'S':
                    user.is_student = True
                else:
                    user.is_teacher = True
                user.save()
                return redirect('index')

        else:
            signup_form = SignupForm()
        return render(request, "signup.html", {"signup_form": signup_form})


def login_user(request):
    """Attempts to log in existing user"""
    if request.user.is_authenticated: 
        return redirect('dashboard')
    else:
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
                        if request.user.is_authenticated:
                            return redirect('index')
            except:
                import traceback
                traceback.print_exc()
                return render(request, "login.html", {"login_form": login_form})

        else:
            login_form = LoginForm()
        return render(request, "login.html", {"login_form": login_form})


def logout_user(request):
    """If user is logged in, logs them out. Then redirects to landing page."""
    if request.user.is_authenticated:
        print(f"Logging out user {request.user.username}")
        logout(request)
    else:
        print("No authenticated users found")

    return redirect('index')
