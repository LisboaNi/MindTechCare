import requests


def get_github_commits(username, repo, token=None):
    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    headers = {}

    if token:
        headers["Authorization"] = f"token {token}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commits = response.json()
        commit_list = []
        for commit in commits:
            commit_data = {
                "message": commit["commit"]["message"],
                "date": commit["commit"]["author"]["date"],
                "author": {
                    "login": commit["author"]["login"] if commit.get("author") else None
                },
            }
            commit_list.append(commit_data)
        return commit_list
    else:
        return {"error": "Não foi possível obter os commits"}
