import requests


def get_github_commits(username, repo, token=None):
    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    headers = {}

    if token:
        headers["Authorization"] = f"token {token}"

    commit_list = []
    page = 1
    while True:
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})

        if response.status_code == 200:
            commits = response.json()
            if not commits:  # Se não houver mais commits, sai do loop
                break

            for commit in commits:
                commit_data = {
                    "message": commit["commit"]["message"],
                    "date": commit["commit"]["author"]["date"],
                    "author": {
                        "login": commit["author"]["login"] if commit.get("author") else None
                    },
                }
                commit_list.append(commit_data)

            page += 1  # Avança para a próxima página
        else:
            return {"error": "Não foi possível obter os commits"}

    return commit_list
