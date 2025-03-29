from django import forms
from .models import UserModel

class UserModelForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['name', 'cnpj', 'email', 'password']

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Senha", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )