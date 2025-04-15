from django import forms
from django.contrib.auth import authenticate
from .models import UserModel
from django.contrib.auth.forms import AuthenticationForm


class UserModelForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Digite sua nova senha"}),
        label="Senha",
    )

    class Meta:
        model = UserModel
        fields = ["name", "cnpj", "email", "password"]


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Email"

    pass
