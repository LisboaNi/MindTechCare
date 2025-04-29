from django import forms
from .models import UserModel
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

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
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if password:
            try:
                validate_password(password)  # Usa validação padrão do Django
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        
        return password


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Email"

    pass
