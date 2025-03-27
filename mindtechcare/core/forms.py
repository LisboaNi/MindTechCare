# forms.py
from django import forms
from .models import Empresa, Profissional

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome', 'cnpj', 'email', 'senha']


class LoginEmpresaForm(forms.Form):
    email = forms.EmailField(label="Email")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)

    
class ProfissionalForm(forms.ModelForm):
    class Meta:
        model = Profissional
        fields = ['nome', 'cargo']
