from django import forms
from django.contrib.auth import authenticate
from .models import UserModel


class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    class Meta:
        model = UserModel
        fields = ['name', 'cnpj', 'email', 'password']


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Email ou senha inválidos.")
            if not user.is_active:
                raise forms.ValidationError("Este usuário está desativado.")
        return cleaned_data
