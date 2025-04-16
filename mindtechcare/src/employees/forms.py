# forms.py
from django import forms
from .models import Employee
from django.contrib.auth.forms import AuthenticationForm


class EmployeeForm(forms.ModelForm):

    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome"}),
        label="Nome",
    )

    email = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "Digite o email"})
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Digite a senha"}),
        label="Senha",
    )

    function = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Digite a função"}),
        label="Função",
    )

    class Meta:
        model = Employee
        fields = ["name", "email", "password", "function"]


class EmployeeLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Email"

    pass


class TokenForm(forms.ModelForm):
    trello_token = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Cole aqui seu  novo token do Trello"}
        ),
        label="Token Trello",
    )
    github_token = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Cole aqui seu novo token do GitHub"}
        ),
        label="Token GitHub",
    )

    class Meta:
        model = Employee
        fields = ["trello_username", "trello_token", "github_username", "github_token"]
