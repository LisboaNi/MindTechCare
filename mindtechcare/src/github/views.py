# views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View
from django.http import JsonResponse
from django.views import View
from .models import RepositorioGitHub, AtividadeGitHub
from .forms import RepositorioGitHubForm, AtividadeGitHubForm
from .integrations import get_github_commits
from employees.models import Employee


# CRUD para RepositorioGitHub
class RepositorioCreateView(CreateView):
    model = RepositorioGitHub
    form_class = RepositorioGitHubForm
    template_name = 'github/repositorio_create.html'
    success_url = reverse_lazy('repositorio_list')

    def form_valid(self, form):
        repo = form.save(commit=False) 
        employee_instance = Employee.objects.get(user=self.request.user)
        repo.employee = employee_instance
        repo.save()
        return super().form_valid(form)


class RepositorioUpdateView(UpdateView):
    model = RepositorioGitHub
    form_class = RepositorioGitHubForm
    template_name = 'github/repositorio_update.html'
    success_url = reverse_lazy('repositorio_list')


class RepositorioDeleteView(DeleteView):
    model = RepositorioGitHub
    template_name = 'github/repositorio_confirm_delete.html'
    success_url = reverse_lazy('repositorio_list')


class RepositorioListView(ListView):
    model = RepositorioGitHub
    template_name = 'github/repositorio_list.html'
    context_object_name = 'repositorios'

    def get_queryset(self):
        """Filtra os repositórios apenas do employee logado."""
        return RepositorioGitHub.objects.filter(employee__user=self.request.user)

# CRUD para AtividadeGitHub
class AtividadeCreateView(CreateView):
    model = AtividadeGitHub
    form_class = AtividadeGitHubForm
    template_name = 'github/atividade_create.html'
    success_url = reverse_lazy('atividade_list')


class AtividadeUpdateView(UpdateView):
    model = AtividadeGitHub
    form_class = AtividadeGitHubForm
    template_name = 'github/atividade_update.html'
    success_url = reverse_lazy('atividade_list')


class AtividadeDeleteView(DeleteView):
    model = AtividadeGitHub
    template_name = 'github/atividade_confirm_delete.html'
    success_url = reverse_lazy('atividade_list')


class AtividadeListView(ListView):
    model = AtividadeGitHub
    template_name = 'github/atividade_list.html'
    context_object_name = 'atividades'


# View para Atualizar Commits do GitHub (integrada com a API do GitHub)
class AtualizarCommitsView(View):
     def post(self, request):
        employee = request.user.employees
        repositorios = RepositorioGitHub.objects.filter(employee=employee)

        total_commits = 0
        for repo in repositorios:
            token = repo.git_token if repo.git_token else None
            commits = get_github_commits(repo.github_username, repo.nome_repositorio, token)

            if "error" in commits:
                continue

            for commit in commits:
                criado, _ = AtividadeGitHub.objects.get_or_create(
                    employee=employee,
                    commit_mensagem=commit["message"],
                    data_commit=commit["date"]
                )
                if criado:
                    total_commits += 1

        return JsonResponse({"success": f"{total_commits} commits atualizados."})