from django.contrib import admin
from accounts.models import UserModel
from employees.models import Employee
from github.models import RepositorioGitHub, AtividadeGitHub

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email',  'created_at') 
    search_fields = ('name', 'email')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'function',  'created_at') 
    search_fields = ('name', 'email')

@admin.register(AtividadeGitHub)
class AtividadeGitHubAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'commit_mensagem', 'data_commit') 

@admin.register(RepositorioGitHub)
class RepositorioGitHub(admin.ModelAdmin):
    list_display = ('id', 'employee', 'nome_repositorio', 'github_username') 


