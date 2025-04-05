# forms.py
from django import forms
from .models import Employee
from django.contrib.auth.forms import AuthenticationForm


class EmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Employee
        fields = ['name', 'email', 'password', 'function']

class EmployeeLoginForm(AuthenticationForm):
    pass 

class TokenForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['trello_username','trello_token', 'github_username', 'github_token']
        widgets = {
            'trello_token': forms.TextInput(attrs={'placeholder': 'Cole aqui seu token do Trello'}),
        }