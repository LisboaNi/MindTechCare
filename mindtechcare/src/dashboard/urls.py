from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardGeralView.as_view(), name='dashboard_geral'),
    path('employee/<int:pk>/', views.DashboardFuncionarioView.as_view(), name='dashboard_funcionario'),
]
