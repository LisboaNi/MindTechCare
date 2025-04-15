from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    FormView,
    View,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserModel
from .forms import UserModelForm, UserLoginForm
from .serializers import UserModelSerializer


# UserModel API ViewSet
class UserModelViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]


# Login
class UserLoginView(FormView):
    template_name = "accounts/login.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        email = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            # Verifica se o usuário tem UserModel (ou seja, não é Employee)
            if not hasattr(user, "usermodel"):
                form.add_error(
                    None,
                    "Apenas empresas podem acessar este sistema.",
                )
                return self.form_invalid(form)

            login(self.request, user)
            return super().form_valid(form)

        form.add_error(None, "Email ou senha inválidos.")
        return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy("user_profile")


# Logout
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


# Profile
class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = "accounts/user_profile.html"
    context_object_name = "profile"

    def get_object(self):
        return self.request.user.usermodel


# Create User
class UserCreateView(CreateView):
    model = UserModel
    form_class = UserModelForm
    template_name = "accounts/user_create.html"
    success_url = reverse_lazy("login")


# Edit User
class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserModel
    form_class = UserModelForm
    template_name = "accounts/user_edit.html"
    success_url = reverse_lazy("user_profile")

    def form_valid(self, form):
        profile_image = self.request.FILES.get("profile_image")
        if profile_image:
            form.instance.profile_image = profile_image
            print("Profile image updated successfully.")
        return super().form_valid(form)

    def form_valid(self, form):
        profile_image = self.request.FILES.get('profile_image')
        if profile_image:
            form.instance.profile_image = profile_image
            print("Imagem atualizada no model!")

        return super().form_valid(form)

    def get_object(self):
        return self.request.user.usermodel

    def test_func(self):
        return self.request.user == self.get_object().user


# Delete User
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserModel
    template_name = "accounts/user_delete.html"
    success_url = reverse_lazy("login")

    def get_object(self):
        return self.request.user.usermodel

    def test_func(self):
        return self.request.user == self.get_object().user

    def post(self, request, *args, **kwargs):
        user_model_instance = self.get_object()
        user = user_model_instance.user

        # Faz logout do usuário
        logout(request)

        # Deleta o UserModel e depois o User padrão
        user_model_instance.delete()
        user.delete()

        return redirect(self.success_url)
