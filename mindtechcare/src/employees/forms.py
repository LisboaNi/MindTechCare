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