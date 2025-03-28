from django import forms
from .models import UserModel

class UserModelForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['name', 'cnpj', 'email', 'password']
