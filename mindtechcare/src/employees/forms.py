# forms.py
from django import forms
from .models import Employee
from django.contrib.auth.forms import AuthenticationForm


class EmployeeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua nova senha'}),
        label="Senha"
    )

    class Meta:
        model = Employee
        fields = ['name', 'email', 'password', 'function']


class EmployeeLoginForm(AuthenticationForm):
    pass


class TokenForm(forms.ModelForm):
    trello_token = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Cole aqui seu  novo token do Trello'}),
        label="Token Trello"
    )
    github_token = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Cole aqui seu novo token do GitHub'}),
        label="Token GitHub"
    )

    class Meta:
        model = Employee
        fields = ['trello_username', 'trello_token', 'github_username', 'github_token']
