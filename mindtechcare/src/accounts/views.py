from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, FormView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserModel
from .forms import UserModelForm, UserLoginForm
from .serializers import UserModelSerializer
from django.contrib.auth import logout

# UserModel API ViewSet
class UserModelViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]

# Login
class UserLoginView(FormView):
    template_name = "accounts/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy('user_profile')

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Email ou senha inválidos.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

# Logout
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# Profile
class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/user_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.usermodel

# Create User
class UserCreateView(CreateView):
    model = UserModel
    form_class = UserModelForm
    template_name = 'accounts/user_create.html'
    success_url = reverse_lazy('login')

# Edit User
class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserModel
    form_class = UserModelForm
    template_name = 'accounts/user_edit.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        return self.request.user.usermodel

    def test_func(self):
        return self.request.user == self.get_object().user

# Delete User
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/user_delete.html'
    success_url = reverse_lazy('login')

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

