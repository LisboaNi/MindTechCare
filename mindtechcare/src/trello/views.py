from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .integrations import get_trello_cards, get_trello_lists

from .models import BoardTrello, CardTrello
from .forms import BoardTrelloForm, CardTrelloForm
from employees.models import Employee
from django.contrib import messages

# CRUD para BoardTrello
class BoardTrelloCreateView(CreateView):
    model = BoardTrello
    form_class = BoardTrelloForm
    template_name = 'trello/board_trello_create.html'
    success_url = reverse_lazy('board-list')

    def form_valid(self, form):
        repo = form.save(commit=False) 
        employee_instance = Employee.objects.get(user=self.request.user)
        repo.employee = employee_instance
        repo.save()
        return super().form_valid(form)

class BoardTrelloListView(ListView):
    model = BoardTrello
    template_name = 'trello/board_trello_list.html'
    context_object_name = 'boards'

    def get_queryset(self):
        """Filtra os repositórios apenas do employee logado."""
        return BoardTrello.objects.filter(employee__user=self.request.user)

class BoardTrelloUpdateView(UpdateView):
    model = BoardTrello
    form_class = BoardTrelloForm
    template_name = 'trello/board_trello_update.html'
    success_url = reverse_lazy('board-list')

class BoardTrelloDeleteView(DeleteView):
    model = BoardTrello
    template_name = 'trello/board_trello_confirm_delete.html'
    success_url = reverse_lazy('board-list')

# CRUD para CardTrello
class CardTrelloCreateView(CreateView):
    model = CardTrello
    form_class = CardTrelloForm
    template_name = 'card_trello_create.html'
    success_url = reverse_lazy('card-list')

    def form_valid(self, form):
        repo = form.save(commit=False) 
        employee_instance = Employee.objects.get(user=self.request.user)
        repo.employee = employee_instance
        repo.save()
        return super().form_valid(form)

class CardTrelloListView(ListView):
    model = CardTrello
    template_name = 'card_trello_list.html'
    context_object_name = 'cards'

    def get_queryset(self):
        return CardTrello.objects.filter(board__employee=self.request.user.employee)

class CardTrelloUpdateView(UpdateView):
    model = CardTrello
    form_class = CardTrelloForm
    template_name = 'card_trello_update.html'
    success_url = reverse_lazy('card-list')

class CardTrelloDeleteView(DeleteView):
    model = CardTrello
    template_name = 'card_trello_confirm_delete.html'
    success_url = reverse_lazy('card-list')

# Atualizar Cards do Trello
import logging

logger = logging.getLogger(__name__)

class AtualizarCardsTrelloView(View):
    def post(self, request, board_id):
        try:
            # Tenta encontrar o board com o ID fornecido
            board = BoardTrello.objects.get(trello_board_id=board_id)
        except BoardTrello.DoesNotExist:
            logger.error(f"Board com ID {board_id} não encontrado.")
            return JsonResponse({"error": "Board não encontrado."}, status=404)

        # Obtém o nome de usuário do Trello associado ao funcionário
        trello_username = board.employee.trello_username
        if not trello_username:
            logger.error(f"Funcionário do board {board_id} não tem Trello username.")
            return JsonResponse({"error": "Funcionário não possui Trello username cadastrado."}, status=400)

        trello_username = trello_username.lower()

        # Obtém as listas do Trello
        lists = get_trello_lists(board.trello_board_id, board.trello_token)
        if "error" in lists:
            logger.error(f"Erro ao obter listas do Trello para o board {board_id}: {lists}")
            return JsonResponse(lists, status=400)

        # Pega o ID da última coluna
        ultima_coluna = lists[-1]["id"]

        # Obtém os cards do Trello
        cards = get_trello_cards(board.trello_board_id, board.trello_token)
        if "error" in cards:
            logger.error(f"Erro ao obter cards do Trello para o board {board_id}: {cards}")
            return JsonResponse(cards, status=400)

        count = 0
        for card in cards:
            # Ignora cards arquivados
            if card.get("closed", False):
                continue

            # Ignora cards que estão na última coluna
            if card["idList"] == ultima_coluna:
                continue

            # Verifica se o nome ou descrição do card contém o username
            nome_card = card["name"].lower()
            descricao_card = (card.get("desc") or "").lower()

            if trello_username not in nome_card and trello_username not in descricao_card:
                continue

            # Cria o card no banco de dados se ele ainda não existir
            if not CardTrello.objects.filter(trello_card_id=card["id"]).exists():
                CardTrello.objects.create(
                    employee=board.employee,
                    board=board,
                    nome_card=card["name"],
                    data_criacao=card["dateLastActivity"],
                    trello_card_id=card["id"]
                )
                count += 1

        # Loga a quantidade de cards salvos
        logger.info(f"{count} cards salvos para o usuário {trello_username} no board {board_id}.")
        return JsonResponse({"success": f"{count} Cards atualizados com sucesso!"})
