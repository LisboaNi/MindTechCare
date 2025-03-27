from django.urls import path
from .views import github_dashboard, jira_dashboard
from .import views

urlpatterns = [
    path('github/', github_dashboard, name='github_dashboard'),
    path('jira/', jira_dashboard, name='jira_dashboard'),
    path('cadastro/', views.cadastro_empresa, name='cadastro_empresa'),
    path('login/', views.login_empresa, name='login_empresa'),
    path('perfil/', views.perfil_empresa, name='perfil_empresa'),
    path('cadastrar-profissional/', views.cadastrar_profissional, name='cadastrar_profissional'),
    path('perfil_profissional/<int:profissional_id>/', views.perfil_profissional, name='perfil_profissional'),
    path('', views.index, name='index'),
]
