import requests
from .models import AtividadeGitHub, RepositorioGitHub

GITHUB_TOKEN = "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"

def get_github_commits(username, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commits = response.json()
        commit_list = []
        for commit in commits:
            commit_data = {
                "message": commit["commit"]["message"],
                "date": commit["commit"]["author"]["date"],
            }
            commit_list.append(commit_data)

            # Salvar no banco de dados
            employee = RepositorioGitHub.objects.get(github_username=username, nome_repositorio=repo).employee
            AtividadeGitHub.objects.create(
                employee=employee,
                commit_mensagem=commit_data['message'],
                data_commit=commit_data['date']
            )
        return commit_list
    else:
        return {"error": "Não foi possível obter os commits"}
