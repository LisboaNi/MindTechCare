from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import UserModel
from employees.models import Employee
from .forms import LoginForm  # Certifique-se de que o formulário está correto

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                # Verifica se o usuário é do tipo UserModel ou Employee
                if UserModel.objects.filter(user=user).exists():
                    return redirect("user_list")  # Redireciona para o dashboard do UserModel
                elif Employee.objects.filter(user=user).exists():
                    return redirect("employee_profile")  # Redireciona para o dashboard do Employee
                else:
                    return redirect("login")  # Se não for nenhum dos dois, redireciona para login ou outra página

            else:
                # Verifica se o email existe no banco
                if not User.objects.filter(username=email).exists():
                    form.add_error(None, "Cadastro não encontrado. Verifique seu email.")
                else:
                    form.add_error(None, "Email ou senha inválidos.")
    else:
        form = LoginForm()

    return render(request, "login/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
