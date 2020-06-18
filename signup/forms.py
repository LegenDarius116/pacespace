from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django import forms
from database.models import PaceUser
from django.utils.safestring import mark_safe

class SignupForm(UserCreationForm):
    USERTYPE_CHOICES = [
        ('S', 'I am a student'),
        ('T', 'I am a teacher'),
    ]

    usertype = forms.ChoiceField(
        label=mark_safe('<br/> <br/> Usertype'), 
        choices=USERTYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': "usertype"}),
        help_text=None,
    )

    class Meta(UserCreationForm.Meta):
        model = PaceUser
        help_texts = {
            'username': None,
        }
        fields = ["username","first_name", "last_name", "email", "password1", "password2"]
