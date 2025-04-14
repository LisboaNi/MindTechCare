# views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponseForbidden
from .models import RepositorioGitHub, AtividadeGitHub
from .forms import RepositorioGitHubForm, AtividadeGitHubForm
from .integrations import get_github_commits
from employees.models import Employee
from validations.validators import decrypt_token


# CRUD para RepositorioGitHub
class RepositorioCreateView(CreateView):
    model = RepositorioGitHub
    form_class = RepositorioGitHubForm
    template_name = "github/repositorio_create.html"
    success_url = reverse_lazy("repositorio_list")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            try:
                employee_instance = Employee.objects.get(user=self.request.user)
                repo = form.save(commit=False)
                repo.employee = employee_instance
                repo.save()
                return super().form_valid(form)
            except Employee.DoesNotExist:
                form.add_error(
                    None, "Não foi possível associar o repositório ao seu funcionário."
                )
                return super().form_invalid(form)
        else:
            return HttpResponseForbidden("Usuário não autenticado.")


class RepositorioUpdateView(UpdateView):
    model = RepositorioGitHub
    form_class = RepositorioGitHubForm
    template_name = "github/repositorio_update.html"
    success_url = reverse_lazy("repositorio_list")


class RepositorioDeleteView(DeleteView):
    model = RepositorioGitHub
    template_name = "github/repositorio_confirm_delete.html"
    success_url = reverse_lazy("repositorio_list")


class RepositorioListView(ListView):
    model = RepositorioGitHub
    template_name = "github/repositorio_list.html"
    context_object_name = "repositorios"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            try:
                employee_instance = Employee.objects.get(user=self.request.user)
                return RepositorioGitHub.objects.filter(employee=employee_instance)
            except Employee.DoesNotExist:
                return RepositorioGitHub.objects.none()  # Retorna um queryset vazio
        else:
            return RepositorioGitHub.objects.none()


# CRUD para AtividadeGitHub
class AtividadeCreateView(CreateView):
    model = AtividadeGitHub
    form_class = AtividadeGitHubForm
    template_name = "github/atividade_create.html"
    success_url = reverse_lazy("atividade_list")


class AtividadeUpdateView(UpdateView):
    model = AtividadeGitHub
    form_class = AtividadeGitHubForm
    template_name = "github/atividade_update.html"
    success_url = reverse_lazy("atividade_list")


class AtividadeDeleteView(DeleteView):
    model = AtividadeGitHub
    template_name = "github/atividade_confirm_delete.html"
    success_url = reverse_lazy("atividade_list")


class AtividadeListView(ListView):
    model = AtividadeGitHub
    template_name = "github/atividade_list.html"
    context_object_name = "atividades"


# View para Atualizar Commits do GitHub (integrada com a API do GitHub)
class AtualizarCommitsView(View):
    def post(self, request):
        employee = request.user.employees
        github_username = employee.github_username
        github_token = decrypt_token(employee.github_token)

        if not github_username:
            return JsonResponse(
                {"error": "GitHub username não configurado no perfil."}, status=400
            )

        repositorios = employee.repositorios.all()
        total_commits = 0

        for repo in repositorios:
            commits = get_github_commits(
                github_username, repo.nome_repositorio, github_token
            )

            if "error" in commits:
                continue

            # Filtrar apenas os commits feitos pelo github_username do employee
            for commit in commits:
                commit_author = commit.get("author")
                if commit_author and commit_author.get("login") == github_username:
                    criado, _ = AtividadeGitHub.objects.get_or_create(
                        employee=employee,
                        commit_mensagem=commit["message"],
                        data_commit=commit["date"],
                    )
                    if criado:
                        total_commits += 1

        return JsonResponse({"success": f"{total_commits} commits atualizados."})
