# views.py
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.permissions import IsAuthenticated

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]  # Garantir que só usuários logados acessem

    def perform_create(self, serializer):
        # Criar Employee com o usuário logado
        serializer.save(accounts=self.request.user)

# views.py (para views tradicionais)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import EmployeeForm, EmployeeLoginForm # Presumindo que você tenha um formulário para Employees
from accounts.models import UserModel
from django.contrib.auth.models import User

def employee_login(request):
    if request.method == "POST":
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("employee_profile")
            else:
                try:
                    user_exists = User.objects.filter(username=email).exists()
                    if not user_exists:
                        form.add_error(
                            None, "Cadastro não encontrado. Verifique seu email."
                        )
                    else:
                        form.add_error(None, "Email ou senha inválidos.")
                except User.DoesNotExist:
                    form.add_error(
                        None, "Erro ao verificar o usuário. Tente novamente."
                    )
        else:
            form.add_error(None, "Dados inválidos!")
    else:
        form = EmployeeLoginForm()
    return render(request, "employees/login.html", {"form": form})

@login_required
def employee_logout(request):
    logout(request)
    return redirect("employee_list")

@login_required
def employee_profile(request):
    user = request.user
    employees = Employee.objects.filter(user=user).first()
    return render(request, "employees/employee_profile.html", {'employees': employees})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)  # Não salva ainda
            user_model_instance = UserModel.objects.get(user=request.user)  # Ou outra lógica de busca do UserModel
            employee.accounts = user_model_instance  # Associa o UserModel ao Employee
            employee.save()  # Salva o Employee com o accounts preenchido
            return redirect('employee_list')  # Redireciona para a página de perfil após a criação
    else:
        form = EmployeeForm()
    
    return render(request, 'employees/employee_create.html', {'form': form})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

def employee_edit(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_edit.html', {'form': form, 'employee': employee})

def employee_delete(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        if employee.user:
                employee.user.delete()
        return redirect('employee_list')
    return render(request, 'employees/employee_delete.html', {'employee': employee})
