from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required

from .integrations import get_github_commits, get_jira_tasks
from .forms import EmpresaForm, LoginEmpresaForm, ProfissionalForm
from .models import Profissional, Empresa



def github_dashboard(request):
    commits = get_github_commits("usuario_github", "repositorio")
    return render(request, "github_dashboard.html", {"commits": commits})

def jira_dashboard(request):
    tasks = get_jira_tasks()
    return render(request, "jira_dashboard.html", {"tasks": tasks})

def cadastro_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()  # O método save do formulário já vai criar a Empresa e o User
            return redirect('login_empresa')  # Redireciona para a página de login
    else:
        form = EmpresaForm()
    
    return render(request, 'cadastro_empresa.html', {'form': form})

def login_empresa(request):
    if request.method == 'POST':
        form = LoginEmpresaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            
            # Buscar a empresa pelo email
            try:
                empresa = Empresa.objects.get(email=email)  # Busca a empresa pelo email
                # Autentica a empresa com email e senha
                user = authenticate(request, username=email, password=senha)
                if user is not None and user == empresa.user:  # Verifica se o user existe e é o correto
                    login(request, user)  # Realiza o login
                    return redirect('perfil_empresa')  # Redireciona para o perfil da empresa
                else:
                    form.add_error(None, 'Email ou senha inválidos')  # Se a senha estiver errada ou o usuário não for encontrado
            except Empresa.DoesNotExist:
                form.add_error(None, 'Email não encontrado')  # Caso não encontre a empresa pelo email

    else:
        form = LoginEmpresaForm()

    return render(request, 'login_empresa.html', {'form': form})

@login_required
def cadastrar_profissional(request):
    empresa = request.user.empresa  # Supondo que você tenha configurado um perfil de empresa para o usuário

    if request.method == 'POST':
        form = ProfissionalForm(request.POST)
        if form.is_valid():
            profissional = form.save(commit=False)
            profissional.empresa = empresa  # Associando o profissional à empresa logada
            profissional.save()
            return redirect('perfil_empresa')  # Redireciona para o perfil da empresa
    else:
        form = ProfissionalForm()

    return render(request, 'cadastrar_profissional.html', {'form': form})

@login_required
def perfil_empresa(request):
    empresa = request.user.empresa  # Supondo que o usuário tenha um perfil de empresa
    profissionais = Profissional.objects.filter(empresa=empresa)
    return render(request, 'perfil_empresa.html', {'empresa': empresa, 'profissionais': profissionais})
