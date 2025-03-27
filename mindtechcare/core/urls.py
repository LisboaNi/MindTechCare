from django.urls import path
from .views import github_dashboard, jira_dashboard

urlpatterns = [
    path('github/', github_dashboard, name='github_dashboard'),
    path('jira/', jira_dashboard, name='jira_dashboard'),
]
