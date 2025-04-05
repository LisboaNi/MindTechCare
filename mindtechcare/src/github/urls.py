from django.urls import path
from .views import (
    RepositorioCreateView, RepositorioUpdateView, RepositorioDeleteView, RepositorioListView,
    # AtividadeCreateView, AtividadeUpdateView, AtividadeDeleteView, AtividadeListView,
    AtualizarCommitsView
)

urlpatterns = [
    path('repositorio/create/', RepositorioCreateView.as_view(), name='repositorio_create'),
    path('repositorio/update/<int:pk>/', RepositorioUpdateView.as_view(), name='repositorio_update'),
    path('repositorio/delete/<int:pk>/', RepositorioDeleteView.as_view(), name='repositorio_delete'),
    path('repositorios/', RepositorioListView.as_view(), name='repositorio_list'),
    
    # path('atividade/create/', AtividadeCreateView.as_view(), name='atividade_create'),
    # path('atividade/update/<int:pk>/', AtividadeUpdateView.as_view(), name='atividade_update'),
    # path('atividade/delete/<int:pk>/', AtividadeDeleteView.as_view(), name='atividade_delete'),
    # path('atividades/', AtividadeListView.as_view(), name='atividade_list'),

    path('employee/github/update-all/', AtualizarCommitsView.as_view(), name='atualizar_todos_commits'),

]
