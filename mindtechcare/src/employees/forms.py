# forms.py
from django import forms
from .models import Employee
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class EmployeeForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Digite o nome"}),
        label="Nome",
    )

    email = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Digite o email"})
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Digite a senha"}),
        label="Senha",
    )

    function = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Digite a função"}),
        label="Função",
    )

    class Meta:
        model = Employee
        fields = ["name", "email", "password", "function"]
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if password:
            try:
                validate_password(password)  # Usa validação padrão do Django
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        
        return password
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:
            self.fields["password"].required = True


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
    