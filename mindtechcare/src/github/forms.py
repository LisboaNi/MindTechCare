from django import forms
from .models import RepositorioGitHub, AtividadeGitHub


class RepositorioGitHubForm(forms.ModelForm):
    class Meta:
        model = RepositorioGitHub
        fields = ["nome_repositorio", "github_username"]


class AtividadeGitHubForm(forms.ModelForm):
    class Meta:
        model = AtividadeGitHub
        fields = ["employee", "commit_mensagem", "data_commit"]
