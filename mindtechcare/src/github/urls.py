from django.urls import path
from . import views

urlpatterns = [
    path('repositorio/create/', views.create_repositorio, name='repositorio_create'),
    path('repositorio/<int:pk>/update/', views.update_repositorio, name='repositorio_update'),
    path('repositorio/<int:pk>/delete/', views.delete_repositorio, name='repositorio_delete'),
    path('repositorio/', views.list_repositorios, name='repositorio_list'),

    path('atividade/create/', views.create_atividade, name='atividade_create'),
    path('atividade/<int:pk>/update/', views.update_atividade, name='atividade_update'),
    path('atividade/<int:pk>/delete/', views.delete_atividade, name='atividade_delete'),
    path('atividade/', views.list_atividades, name='atividade_list'),
]
