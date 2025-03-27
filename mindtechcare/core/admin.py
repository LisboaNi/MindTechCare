from django.contrib import admin
from .models import Empresa, Profissional, AtividadeGitHub, TarefaJira

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'criado_em')
    search_fields = ('nome', 'cnpj')
    list_filter = ('criado_em',)

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'empresa', 'criado_em')
    search_fields = ('cargo', 'empresa__nome')
    list_filter = ('empresa', 'criado_em')

@admin.register(AtividadeGitHub)
class AtividadeGitHubAdmin(admin.ModelAdmin):
    list_display = ('profissional', 'commit_mensagem', 'data_commit')
    search_fields = ('profissional__usuario__username', 'commit_mensagem')
    list_filter = ('data_commit',)

@admin.register(TarefaJira)
class TarefaJiraAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'profissional', 'status')
    search_fields = ('titulo', 'profissional__usuario__username')
    list_filter = ('status',)
