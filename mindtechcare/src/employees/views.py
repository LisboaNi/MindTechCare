from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, View, DeleteView
from django.urls import reverse_lazy
from .models import Employee
from .forms import EmployeeForm, EmployeeLoginForm, TokenForm
from accounts.models import UserModel
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from trello.integrations import API_KEY
from django.core.exceptions import ObjectDoesNotExist


# Login
class EmployeeLoginView(LoginView):
    template_name = "employees/login.html"
    form_class = EmployeeLoginForm

    def form_valid(self, form):
        email = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            try:
                # Verifica se é um funcionário de verdade
                _ = user.employees
            except ObjectDoesNotExist:
                form.add_error(None, "Apenas funcionários podem acessar este sistema.")
                return self.form_invalid(form)

            login(self.request, user)
            return super().form_valid(form)

        form.add_error(None, "Email ou senha inválidos.")
        return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy("employee_profile")


# Logout
class EmployeeLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("employee_login")


# Profile
class EmployeeProfileView(DetailView):
    model = Employee
    template_name = "employees/employee_profile.html"
    context_object_name = "employee"

    def get_object(self):
        return get_object_or_404(Employee, user=self.request.user)


# Create Employee
class EmployeeCreateView(LoginRequiredMixin, View):
    template_name = "employees/employee_create.html"

    def get(self, request):
        try:
            empresa = request.user.usermodel  # Conta da empresa logada
        except UserModel.DoesNotExist:
            return redirect(
                "login"
            )  # Se não encontrar a empresa, redireciona para login

        # Verifica o número de funcionários já cadastrados para a empresa
        num_funcionarios = Employee.objects.filter(accounts=empresa).count()

        # Defina o número máximo de funcionários permitidos, por exemplo, 5
        max_funcionarios = (
            empresa.max_funcionarios if hasattr(empresa, "max_funcionarios") else 5
        )

        if num_funcionarios >= max_funcionarios:
            # Redireciona para a tela de compra de acesso se o limite for atingido
            return redirect("buy_access")  # Ajuste o nome da URL conforme necessário

        form = EmployeeForm()  # Exibe o formulário de criação de funcionário
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = EmployeeForm(request.POST)

        if form.is_valid():
            employee = form.save(commit=False)

            try:
                empresa = request.user.usermodel  # Conta da empresa logada
            except UserModel.DoesNotExist:
                form.add_error(None, "Conta de empresa não encontrada.")
                return render(request, self.template_name, {"form": form})

            # Associa o employee à empresa logada
            employee.accounts = empresa
            employee.save()
            return redirect("employee_list")

        return render(request, self.template_name, {"form": form})


# List Employees
class EmployeeListView(ListView):
    model = Employee
    template_name = "employees/employee_list.html"
    context_object_name = "employees"

    def get_queryset(self):
        user = self.request.user
        try:
            user_model = user.usermodel
            return Employee.objects.filter(accounts=user_model)
        except UserModel.DoesNotExist:
            return Employee.objects.none()


# Edit Employee
class EmployeeEditView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employees/employee_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        context["employee"] = employee
        return context

    def get_success_url(self):
        user = self.request.user
        # Se o usuário logado é um UserModel (empresa), redireciona para a lista
        if hasattr(user, "usermodel"):
            return reverse_lazy("employee_list")
        # Senão, redireciona para o perfil do próprio funcionário
        return reverse_lazy("employee_profile")


# Delete Employee
class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = "employees/employee_delete.html"

    def post(self, request, *args, **kwargs):
        employee = self.get_object()
        user = employee.user
        employee.delete()
        if user:
            user.delete()
        return redirect(self.get_success_url())  # Aqui chamamos o método corretamente

    def get_success_url(self):
        user = self.request.user
        # Se o usuário logado é um UserModel (empresa), redireciona para a lista
        if hasattr(user, "usermodel"):
            return reverse_lazy("employee_list")
        # Senão, redireciona para o perfil do próprio funcionário
        return reverse_lazy("employee_profile")


# Token
class TokenUpdateView(UpdateView):
    model = Employee
    form_class = TokenForm
    template_name = "employees/token_edit.html"
    success_url = reverse_lazy("employee_profile")

    def get_object(self):
        return get_object_or_404(Employee, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        context["employee"] = employee

        # Só gera o link se ainda não tiver token
        if not employee.trello_token:
            context["trello_auth_url"] = (
                f"https://trello.com/1/authorize?"
                f"expiration=never&name=MindTechCare"
                f"&scope=read,write&response_type=token&key={API_KEY}"
            )
        return context
