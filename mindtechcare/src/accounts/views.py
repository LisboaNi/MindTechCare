from rest_framework import viewsets
from .models import UserModel
from .serializers import UserModelSerializer
from rest_framework.permissions import IsAuthenticated


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserModel
from .forms import UserModelForm, UserLoginForm
from django.contrib.auth.models import User


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("user_list")
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
        form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})

@login_required
def user_logout(request):
    logout(request)
    return redirect("user_login")

@login_required
def user_list(request):
    user = request.user
    users = UserModel.objects.filter(user=user).first()

    return render(request, "accounts/user_list.html", {"users": users})

def user_create(request):
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = UserModelForm()
    return render(request, 'accounts/user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(UserModel, pk=pk)
    if request.method == 'POST':
        form = UserModelForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserModelForm(instance=user)
    return render(request, 'accounts/user_form.html', {'form': form})

def user_delete(request, pk):
    user_model = get_object_or_404(UserModel, pk=pk)
    
    if request.method == 'POST':
        if user_model.user: 
            user_model.user.delete()  
                
        return redirect('user_login')
    
    return render(request, 'accounts/user_confirm_delete.html', {'user': user_model})

