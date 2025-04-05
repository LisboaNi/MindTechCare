from django.urls import path
from .views import (
    RepositorioCreateView, RepositorioUpdateView, RepositorioDeleteView, RepositorioListView,
    # AtividadeCreateView, AtividadeUpdateView, AtividadeDeleteView, AtividadeListView,
    AtualizarCommitsView
)

urlpatterns = [
    path('create/', RepositorioCreateView.as_view(), name='repositorio_create'),
    path('update/<int:pk>/', RepositorioUpdateView.as_view(), name='repositorio_update'),
    path('delete/<int:pk>/', RepositorioDeleteView.as_view(), name='repositorio_delete'),
    path(' ', RepositorioListView.as_view(), name='repositorio_list'),
    
    # path('atividade/create/', AtividadeCreateView.as_view(), name='atividade_create'),
    # path('atividade/update/<int:pk>/', AtividadeUpdateView.as_view(), name='atividade_update'),
    # path('atividade/delete/<int:pk>/', AtividadeDeleteView.as_view(), name='atividade_delete'),
    # path('atividades/', AtividadeListView.as_view(), name='atividade_list'),

    path('update-all/', AtualizarCommitsView.as_view(), name='atualizar_todos_commits'),

]
