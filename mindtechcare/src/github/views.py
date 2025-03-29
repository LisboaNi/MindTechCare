from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import RepositorioGitHub, AtividadeGitHub
from .forms import RepositorioGitHubForm, AtividadeGitHubForm
from .integrations import get_github_commits
from employees.models import Employee

def create_repositorio(request):
    if request.method == 'POST':
        form = RepositorioGitHubForm(request.POST)
        if form.is_valid():
            repo = form.save(commit=False)  # Não salva ainda
            employee_instance = Employee.objects.get(user=request.user)
            repo.employee = employee_instance
            repo.save()
            return redirect('repositorio_list')  # Redireciona para a lista de repositórios
    else:
        form = RepositorioGitHubForm()
    return render(request, 'github/repositorio_create.html', {'form': form})

def update_repositorio(request, pk):
    repositorio = get_object_or_404(RepositorioGitHub, pk=pk)
    if request.method == 'POST':
        form = RepositorioGitHubForm(request.POST, instance=repositorio)
        if form.is_valid():
            form.save()
            return redirect('repositorio_list')  # Redireciona para a lista de repositórios
    else:
        form = RepositorioGitHubForm(instance=repositorio)
    return render(request, 'github/repositorio_update.html', {'form': form})

def delete_repositorio(request, pk):
    repositorio = get_object_or_404(RepositorioGitHub, pk=pk)
    if request.method == 'POST':
        repositorio.delete()
        return redirect('repositorio_list')  # Redireciona para a lista de repositórios
    return render(request, 'github/repositorio_confirm_delete.html', {'repositorio': repositorio})

def list_repositorios(request):
    repositorios = RepositorioGitHub.objects.all()
    return render(request, 'github/repositorio_list.html', {'repositorios': repositorios})

# CRUD para AtividadeGitHub
def atualizar_commits(request, username, repo):
    # Recupera o repositório usando o username e o nome do repositório
    try:
        repositorio = RepositorioGitHub.objects.get(github_username=username, nome_repositorio=repo)
    except RepositorioGitHub.DoesNotExist:
        return JsonResponse({"error": "Repositório não encontrado."}, status=404)

    # Obtenha o token de autenticação, se presente
    token = repositorio.git_token if repositorio.git_token else None

    # Chama a função que busca os commits usando a API do GitHub
    commits = get_github_commits(username, repo, token)

    if "error" in commits:
        return JsonResponse(commits, status=400)  # Retorna o erro se a requisição falhou

    # Para cada commit retornado pela API, salvar no banco de dados
    for commit in commits:
        # Verifica se o commit já existe para evitar duplicação
        if not AtividadeGitHub.objects.filter(commit_mensagem=commit["message"], data_commit=commit["date"]).exists():
            # Salvar o commit no banco de dados
            AtividadeGitHub.objects.create(
                employee=repositorio.employee,  # Associa ao employee do repositório
                commit_mensagem=commit["message"],
                data_commit=commit["date"]
            )

    # Retorna a lista de commits como resposta
    return JsonResponse(commits, safe=False)


def create_atividade(request):
    if request.method == 'POST':
        form = AtividadeGitHubForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('atividade_list')  # Redireciona para a lista de atividades
    else:
        form = AtividadeGitHubForm()
    return render(request, 'github/atividade_create.html', {'form': form})

def update_atividade(request, pk):
    atividade = get_object_or_404(AtividadeGitHub, pk=pk)
    if request.method == 'POST':
        form = AtividadeGitHubForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            return redirect('atividade_list')  # Redireciona para a lista de atividades
    else:
        form = AtividadeGitHubForm(instance=atividade)
    return render(request, 'github/atividade_update.html', {'form': form})

def delete_atividade(request, pk):
    atividade = get_object_or_404(AtividadeGitHub, pk=pk)
    if request.method == 'POST':
        atividade.delete()
        return redirect('atividade_list')  # Redireciona para a lista de atividades
    return render(request, 'github/atividade_confirm_delete.html', {'atividade': atividade})

def list_atividades(request):
    atividades = AtividadeGitHub.objects.all()
    return render(request, 'github/atividade_list.html', {'atividades': atividades})


