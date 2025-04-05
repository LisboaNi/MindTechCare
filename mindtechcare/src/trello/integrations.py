# integrations.py
import requests

API_KEY = "43370450ff380ecd3ddb2617c30b9841"

def get_trello_cards(board_id, token):
    if not token:
        return {"error": "O token do Trello é obrigatório."}

    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    params = {
        "key": API_KEY,
        "token": token,
        "fields": "name,idList,dateLastActivity,desc",
        "members": "true",
        "member_fields": "username"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return {"error": f"Erro HTTP {response.status_code}: {response.text}"}
    except requests.exceptions.JSONDecodeError:
        return {"error": "Resposta não é um JSON válido"}

def get_trello_lists(board_id, token):
    if not token:
        return {"error": "O token do Trello é obrigatório."}

    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    params = {
        "key": API_KEY,
        "token": token
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return {"error": f"Erro HTTP {response.status_code}: {response.text}"}
    except requests.exceptions.JSONDecodeError:
        return {"error": "Resposta não é um JSON válido"}

def get_card_members(card_id, token):
    if not token:
        return []

    url = f"https://api.trello.com/1/cards/{card_id}/members"
    params = {
        "key": API_KEY,
        "token": token
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return data if isinstance(data, list) else []
    except requests.exceptions.RequestException:
        return []
