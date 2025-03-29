from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import RepositorioGitHub, AtividadeGitHub
from .forms import RepositorioGitHubForm, AtividadeGitHubForm
from .integrations import get_github_commits

# CRUD para RepositorioGitHub
def atualizar_commits(request, username, repo):
    commits = get_github_commits(username, repo)
    return JsonResponse(commits, safe=False)

def create_repositorio(request):
    if request.method == 'POST':
        form = RepositorioGitHubForm(request.POST)
        if form.is_valid():
            form.save()
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
    return render(request, 'repositorio_confirm_delete.html', {'repositorio': repositorio})

def list_repositorios(request):
    repositorios = RepositorioGitHub.objects.all()
    return render(request, 'github/repositorio_list.html', {'repositorios': repositorios})

# CRUD para AtividadeGitHub

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


