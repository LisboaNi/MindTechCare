import requests

GITHUB_TOKEN = "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"

def get_github_commits(username, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commits = response.json()
        return [{"message": commit["commit"]["message"], "date": commit["commit"]["author"]["date"]} for commit in commits]
    else:
        return {"error": "Não foi possível obter os commits"}

JIRA_EMAIL = "nicoli.lisboa@uscsonline.com.br"
JIRA_TOKEN = "ATATT3xFfGF0OnZF1PvxFlDVQFT_PjbwSPJ8jwKQc4nrFUH1AyMOQfAeQwYnUwL-AY39i4LSARqX0BmJZ1-fJ8vz_a-f_jt7W5UirMTcMyohIWsWgZrvyJhVKgf_dW2gQJ3_cX4UPYdsiz3B-QWRfkJ2CQqK_wgSJb3iBmtJ-tXjjzvr08DNMcU=F5C25F74"
JIRA_URL = "https://mindtechcare.atlassian.net/rest/api/3/search"

def get_jira_tasks():
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {JIRA_EMAIL}:{JIRA_TOKEN}"
    }
    query = {"jql": "assignee=currentUser()"}
    
    response = requests.get(JIRA_URL, headers=headers, params=query)
    if response.status_code == 200:
        issues = response.json()["issues"]
        return [{"title": issue["fields"]["summary"], "status": issue["fields"]["status"]["name"]} for issue in issues]
    else:
        return {"error": "Não foi possível obter as tarefas"}


