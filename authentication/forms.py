from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from database.models import PaceUser
from django.utils.safestring import mark_safe

class SignupForm(UserCreationForm):
    USERTYPE_CHOICES = [
        ('S', 'I am a student'),
        ('T', 'I am a teacher'),
    ]

    usertype = forms.ChoiceField(
        label='Usertype',
        choices=USERTYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': "usertype"}),
        help_text=None,
    )

    password2 = forms.CharField(
        label = 'Repeat Password:',
        help_text=None,
        widget=forms.PasswordInput()
    )

    class Meta(UserCreationForm.Meta):
        model = PaceUser
        fields = ["username","first_name", "last_name", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass
