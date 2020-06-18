from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass
