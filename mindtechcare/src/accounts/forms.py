from django import forms
from django.contrib.auth import authenticate
from .models import UserModel
from django.contrib.auth.forms import AuthenticationForm


class UserModelForm(forms.ModelForm):

    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome da Empresa"}),
        label="Nome",
    )

    cnpj = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Digite o CNPJ da empresa"}),
        label="CNPJ",
    )

    email = forms.CharField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "Digite o email"}),
        label="Email",
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Digite sua senha"}),
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
