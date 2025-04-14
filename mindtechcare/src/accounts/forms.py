from django import forms
from django.contrib.auth import authenticate
from .models import UserModel
from django.contrib.auth.forms import AuthenticationForm


class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

    class Meta:
        model = UserModel
        fields = ["name", "cnpj", "email", "password"]


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Email"

    pass
