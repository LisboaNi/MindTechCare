from datetime import datetime
from django.utils import timezone
from .integrations import get_trello_cards, get_trello_lists, get_card_members
from .models import CardTrello

def sync_trello_cards_for_employee(employee):
    boards = employee.boards_trello.all()

    for board in boards:
        listas = get_trello_lists(board.trello_board_id, board.trello_token)
        if not isinstance(listas, list):
            continue

        ultima_lista_id = listas[-1]['id'] if listas else None
        cards = get_trello_cards(board)
        if not isinstance(cards, list):
            continue

        cards_salvos = 0
        cards_removidos = 0
        card_ids_atuais = []

        for card in cards:
            card_id = card['id']
            card_fechado = card.get('closed')
            esta_na_ultima_lista = card['idList'] == ultima_lista_id

            members = get_card_members(card_id, board.trello_token)
            member_usernames = [m.get("username") for m in members] if members else []

            pertence_ao_employee = employee.trello_username in member_usernames

            if card_fechado or esta_na_ultima_lista or not pertence_ao_employee:
                removed, _ = CardTrello.objects.filter(trello_card_id=card_id, employee=employee).delete()
                if removed:
                    cards_removidos += 1
                continue

            data_aware = timezone.make_aware(
                datetime.strptime(card['dateLastActivity'], "%Y-%m-%dT%H:%M:%S.%fZ")
            )

            CardTrello.objects.update_or_create(
                trello_card_id=card_id,
                defaults={
                    "employee": employee,
                    "board": board,
                    "nome_card": card['name'],
                    "data_criacao": data_aware
                }
            )
            cards_salvos += 1
            card_ids_atuais.append(card_id)

        # Limpeza extra
        excluidos = CardTrello.objects.filter(board=board, employee=employee).exclude(trello_card_id__in=card_ids_atuais).delete()[0]
        cards_removidos += excluidos

        print(f"✅ Finalizado: {cards_salvos} cards salvos / {cards_removidos} removidos.")
