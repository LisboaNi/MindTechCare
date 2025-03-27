from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required

from .integrations import get_github_commits, get_jira_tasks
from .forms import EmpresaForm, LoginEmpresaForm, ProfissionalForm, RepositorioGitHubForm
from .models import Profissional, Empresa

def index(request):
    return render(request, 'index.html')

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
            try:
                empresa = Empresa.objects.get(email=email) 
                user = authenticate(request, username=email, password=senha)
                if user is not None and user == empresa.user:  
                    login(request, user)  
                    return redirect('perfil_empresa')  
                else:
                    form.add_error(None, 'Email ou senha inválidos')  
            except Empresa.DoesNotExist:
                form.add_error(None, 'Email não encontrado') 

    else:
        form = LoginEmpresaForm()

    return render(request, 'login_empresa.html', {'form': form})

@login_required
def cadastrar_profissional(request):
    empresa = request.user.empresa  # Supondo que você tenha um perfil de empresa para o usuário

    if request.method == 'POST':
        form = ProfissionalForm(request.POST)
        if form.is_valid():
            # Salva o profissional e associa à empresa
            profissional = form.save(commit=False)
            profissional.empresa = empresa
            profissional.save()

            # Agora, cria o formulário para os repositórios
            repositorio_form = RepositorioGitHubForm(request.POST)
            if repositorio_form.is_valid():
                repositorio = repositorio_form.save(commit=False)
                repositorio.profissional = profissional  # Associa o repositório ao profissional
                repositorio.save()

            return redirect('perfil_empresa')  # Redireciona para o perfil da empresa
    else:
        form = ProfissionalForm()
        repositorio_form = RepositorioGitHubForm()

    return render(request, 'cadastrar_profissional.html', {'form': form, 'repositorio_form': repositorio_form})

@login_required
def perfil_empresa(request):
    empresa = request.user.empresa  
    profissionais = Profissional.objects.filter(empresa=empresa)
    return render(request, 'perfil_empresa.html', {'empresa': empresa, 'profissionais': profissionais})

@login_required
def perfil_profissional(request, profissional_id):
    # Buscar o profissional pelo ID
    profissional = get_object_or_404(Profissional, id=profissional_id)

    return render(request, 'perfil_profissional.html', {'profissional': profissional})