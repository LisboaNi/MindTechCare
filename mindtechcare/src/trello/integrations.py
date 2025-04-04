import requests

api_key = "43370450ff380ecd3ddb2617c30b9841"
token = "106b715177c6e822ba93f9742a2cb83c0d9522fe0ec427602b185f69501299d4"

def get_trello_cards(board_id, token, api_key):
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    params = {
        "key": api_key,
        "token": token
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Não foi possível obter os cards do Trello"}

