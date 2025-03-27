from django.shortcuts import render
from .integrations import get_github_commits, get_jira_tasks

def github_dashboard(request):
    commits = get_github_commits("usuario_github", "repositorio")
    return render(request, "github_dashboard.html", {"commits": commits})

def jira_dashboard(request):
    tasks = get_jira_tasks()
    return render(request, "jira_dashboard.html", {"tasks": tasks})
