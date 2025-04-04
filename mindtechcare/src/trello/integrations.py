import requests

API_KEY = "43370450ff380ecd3ddb2617c30b9841"

def get_trello_cards(board):
    if not board.trello_token:
        return {"error": "O board ainda não foi autorizado no Trello"}

    url = f"https://api.trello.com/1/boards/{board.trello_board_id}/cards"
    params = {
        "key": API_KEY,
        "token": board.trello_token,
        "fields": "name,idList,dateLastActivity,desc"  # inclui descrição
    }

    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return {"error": f"Erro HTTP {response.status_code}: {response.text}"}
    except requests.exceptions.JSONDecodeError:
        return {"error": "Resposta não é um JSON válido"}

def get_trello_lists(board_id, token):
    """Obtém todas as listas (colunas) de um board do Trello."""
    if not token:
        return {"error": "O board ainda não foi autorizado no Trello"}

    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    params = {
        "key": API_KEY,
        "token": token
    }

    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return {"error": f"Erro HTTP {response.status_code}: {response.text}"}
    except requests.exceptions.JSONDecodeError:
        return {"error": "Resposta não é um JSON válido"}
