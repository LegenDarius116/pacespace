from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from database.models import PaceUser
from .forms import SignupForm
from helper import parse_req_body

def signup_view(request):
    print('running signup page')
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        ''' Create user '''
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            usertype = signup_form.cleaned_data["usertype"]
            if usertype is 'S':
                user.is_student = True
            else:
                user.is_teacher = True
            user.save()
#     username = login_form.cleaned_data.get('username')
#     password = login_form.cleaned_data.get('password1')
#     user = authenticate(username=username, password=password)
#     login(request, user)
#     return redirect('home')

    else:
        signup_form = SignupForm()
    return render(request, "signup/signup.html", {"signup_form": signup_form})
